#encoding=UTF-8
import os
import time
from time import gmtime, strftime
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
           'referer': 'https://google.com'}
def create_HTML():
    pass
def replace_nik(a, durl):#замена относительных ссылок на абсолютные
    begin=0
    z=a.find('href="/', begin)
    while z != -1:
        if a[z+7] != "/":
            a=a[:z]+'href="https://'+durl+"/"+a[z+7:]
            begin = z + 7
        else:
            a=a[:z]+'href="https:/'+a[z+7:]
            begin=z+7
        z = a.find('href="/', begin)
    a.replace('///','//')
    return(a)
def spider(URL):
    global index
    if URL.find('/', URL.find('//') + 2) != -1:
        dURL = URL[URL.find('//') + 2:URL.find('/', URL.find('//') + 1)]  # вычленяем доменное имя из адреса сайта
    elif URL.find('?', URL.find('//') + 1) != -1:
        dURL = URL[URL.find('//') + 2:URL.find('?', URL.find('//') + 1)]  # вычленяем имя страницы из адреса сайта
    else:
        dURL = URL[URL.find('//') + 2:]  # вычленяем имя страницы из адреса сайта
    try:
        req = requests.get(URL, headers, timeout=3)
    except requests.exceptions.Timeout:
        return 0
    except requests.exceptions.TooManyRedirects:
        return 0
    except requests.exceptions.RequestException as e:
        return 0
    print(req)
    f1=""
    if req.status_code == 404 :
        print("404")
        return (0)
    req.encoding = 'utf-8'
    data = req.text
    old_end = int(2)
    what = '<a href="'  # зацепка в html коде
    e = ''
    count=0
    domain_text1 = ""
    file = open("result.txt", "r")
    f=file.readlines()
    file.close()
    for i in range(len(f)):
        f[i]=f[i].strip()
    while data.find(what, old_end)!=-1:#Ищем все гиперссылки на странице

        start = data.find(what, old_end)#начало гиперссылки

        end = data.find("\"", start + len(what))  #Конец гиперссылки

        text1 = data[start + len(what):end]#текст ссылки
        old_end = end+1#отрезаем найденную гиперссылку так чтобы цикл работал по оставшемуся файлу
        if text1.find('/', text1.find('//') + 2) != -1: #если гиперссылка абсолютная и в ней есть слеш, то
            domain_text1=text1[text1.find('//') + 2:text1.find('/', text1.find('//') + 2)] #находим адрес домена
        if text1.find('?', text1.find('//') + 2) != -1:#если гиперссылка абсолютная и в ней нет слеша. но есть "?", то
            domain_text1=text1[text1.find('//') + 2:text1.find('?', text1.find('//') + 2)]#находим адрес страницы
        else:#если гиперссылка абсолютная и в ней нет слеша или "?", то
            domain_text1 = text1[text1.find('//') + 1:]#находим адрес страницы

        if e.find(text1)==-1 and text1[:4]=='http' and domain_text1 != dURL:#проверяем ссылку на уникальность
            if text1 not in f:
                e = e + text1 + "\n"
    if keyword in data:
        file3 = open("URL"+URL[8:100].replace("/","_").replace("?","_")+".html", "a", encoding="utf-8")
        print("Bingo!")
        data=replace_nik(data, dURL)
        data.replace('///', '//')
        file3.write(data)
        file3.close()
        file1 = open("found.txt", "a")
        file1.write(URL+"\n")
        index+='<p><a href='+URL+'>'+URL+'</a>'+"</p>\n"
        file1.close()
    file = open("result.txt", "a")
    file.write(e)
    file.close()
    return(count)
global index
index="<!DOCTYPE html>"+"\n"+"<html lang='ru'>"+"\n"+"    <head>"+"\n"+"        <meta charset='utf-8'>"+"\n"+"        <title>Новое исследование</title>"+"\n"+"    </head>"+"\n"+"    <body>"+"\n"+"       <H1>Search results:</H1>"+"\n"
print("Введите ключевую фразу")
keyword=input()
print("Введите адрес сайта с которого начнется поиск")
URL=input()
print("Введите количество страниц на которых будет осуществлен поиск")
COI=int(input())
begin=0
print(spider(URL))
for i in range(COI):
    file = open("result.txt", "r")
    site_list=file.read()
    end=site_list.find('\n', begin)
    print(spider(site_list[begin:end]), site_list[begin:end])
    begin=end+1
index+="    </body>"+"\n"+"</html>"
file=open("index2.html","a")
file.write(index)
file.close()