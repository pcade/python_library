#!/usr/bin/python3
# ============================================================================
# Название: python_library.py
# Родитель: python_library.py
# Автор: Григорий Пахомов
# Версия: 0.1
# Дата: 29.05.2023
# Описание: Это библиотека с вспомогательными скриптами
# ============================================================================

# ============================================================================
# Пример передачи переменных
# ============================================================================

# path      = ~/user/important/scripts
# file_name = python_library.py
# old_str   = 'some text here'
# new_str   = 'some text here'
# find_str  = 'some text here'
# pack_name = lshw
# pip_name = pip

# ============================================================================
# Импорт модулей
# ============================================================================
import sys
import os
import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import threading
import time
import datetime
import re
import subprocess

# ============================================================================
# ============================================================================

# Функция проверки наличия дирректории
def is_dir(path) -> bool:

    if not os.path.isdir(path):
        print(f'{path} - False')
        return(False)
    print(f'{path} - True')
    return(True)

# Функция проверки наличия файла
def is_file(path, file_name) -> bool:

    if is_dir(path) == False:
        return(False)

    if os.path.isfile(path + '/' + file_name) == False:
        print(f'{file_name} in {path} - False')
        return(False)
    print(f'{file_name} in {path} - True')
    return(True)


# ============================================================================
# Функции поиска, подтверждения и записи в файлах
# ============================================================================

# Функция поиска конкретной строки
def parser_str_file(path, file_name, find_str) -> bool:

    a = 0

    if is_file(path, file_name) == False:
        return(False)

    with open(path + '/' + file_name, 'r') as fin:
        lst = fin.readlines()

    for i in lst:
        if find_str in i:
            a += 1
            print(i.rstrip() + '- True')
            return(True)

    if a < 1:
        print(f'{find_str} - False')
        return(False)


# Функция поиска конкретной строки и замена её на иную
def replace_str_file(path, file_name, old_str, new_str) -> bool:

    if is_file(path, file_name) == False:
        return(False)

    if parser_str_file(path, file_name, old_str) == False:
        return(False)

    fin = open(path + '/' + file_name, 'rt')
    data = fin.read()
    data = data.replace(str(old_str), str(new_str))
    fin.close()
    fin = open(path + '/' + file_name, 'wt')
    fin.write(data)
    fin.close()
    return(True)

# Функция поиска конкретной строки и дозаписи следующей строки после неё
def write_doka(path, file_name, old_str, new_str) -> bool:

    if is_file(path, file_name) == False:
        return(False)

    if parser_str_file(path, file_name, old_str) == False:
        return(False)
    
    fin = open(path + '/' + file_name, 'rt')
    data = fin.read()
    data = data.replace(str(old_str) + '\n', str(old_str) + '\n' + str(new_str) + '\n')
    fin.close()
    fin = open(path + '/' + file_name, 'wt')
    fin.write(data)
    fin.close()
    return(True)

# Функция парсинга файла по временным меткам и по содержанию
# path - pwd до файла
# file_name - наименование фала
# start_str - время вхождения в формате 13:30:31
# end_str - время вхождения в формате 13:30:31
# flag - содержащеся значение в искомом промежутке, например 'root'

def parser_auth_log(path, file_name, start_str, end_str, flag) -> str:
    with open(path + '/' + file_name, 'r') as file:

        lst = file.readlines()

        for i in lst:
            if start_str and flag in i:
                print(i.rstrip())
            if end_str in i:
                break
        return(True)

#====================================================================
# Функции проверки установленных компонентов
#====================================================================

# Функции проверки установленных компонентов apt
def apt_pack_checker(package_name)-> bool:
    if os.popen("dpkg -s "+ package_name +" | grep install | awk '{print $2;}'").read().rstrip() == 'install':
        print(f'{ package_name } = True')
        return True
    else:
        print(f'{ package_name } = False')
        return False

# Функция проверки установленных компонентов pip
def pip_pack_checker(pip_pack) -> bool:

    if os.popen('pip3 list | grep -F ' + pip_pack).read().rstrip() != '':
        print(f'{ pip_pack } = True')
        return(True)
    else:
        print(f'пакет { pip_pack } = False')
        return(False)

#====================================================================
# Функции работы с JSON
#====================================================================

# Функция проверки наличия тега 
def parser_tag_json(path, file_name, tag) -> bool:

    if is_file(path, file_name) == False:
        return(False)

    with open(path + '/' + file_name, 'r') as handle:
        json_load = json.load(handle)
        if str(tag) not in json_load:
            print(f"{file_name} {tag} - False")
        else:
            print(f"{file_name} {tag} - True")
    return(True)

# Функция отображения содержимого параметра тега
def parser_tag_param_json(path, file_name, tag) -> bool:

    if is_file(path, file_name) == False:
        return(False)

    if parser_tag_json(path, file_name, tag) == False:
        return(False)

    with open(path + '/' + file_name, 'r') as handle:
        json_load = json.load(handle)
        print(f"{file_name} = {json_load[str(tag)]}")
        return(True)
os.system('ls /path | grep ')
# Функция установки значения параметра в одноуровневом JSON
def change_tag_param_json(path, file_name, tag ,mask) -> bool:

    if is_file(path, file_name) == False:
        return(False)

    if parser_tag_json(path, file_name, tag) == False:
        return(False)

    with open(path + '/' + file_name, 'r') as handle:
        json_load = json.load(handle)
        json_load[tag] = str(mask)
        with open(path + '/' + file_name, 'w') as handle:
            json.dump(json_load, handle, ensure_ascii=False, indent=4)
        print(f"{file_name} {tag} = {json_load[tag]}")
    return(True)

# Функция установки значения параметра в трёхуровневом JSON
def change_3_tag_param_json(path, file_name, tag_1, tag_2, tag_3 ,mask) -> bool:

    if is_file(path, file_name) == False:
        return(False)

    with open(path + '/' + file_name, 'r') as handle:
        json_load = json.load(handle)
        if tag_1 not in json_load:
            print(f"{file_name} {tag_1} = False")
            return(False)
        elif tag_2 not in json_load[str(tag_1)]:
            print(f"{file_name} {tag_2} = False")
            return(False)
        elif tag_3 not in json_load[str(tag_1)][str(tag_2)]:
            print(f"{file_name} {tag_2} = False")
            return(False)
        else:
            json_load[str(tag_1)][str(tag_2)][str(tag_3)] = str(mask)
            with open(path + '/' + file_name, 'w') as handle:
                json.dump(json_load, handle, ensure_ascii=False, indent=4)
            print(f"{file_name} {tag_3} = {json_load[str(tag_1)][str(tag_2)][str(tag_3)]}")
    return(True)

# Функция которая принимает список path1 дирректорий в дирректории path в которой находится json с одинаком названием, но с разным содержанием для вычитки требуемых параметров в список
def parser_json_function(path, path_1, file_1) -> list:
    i = 0
    my_list = []
    while len(path_1) > i:
        with open(path + path_1[i] + '/' + file_1, 'r') as handle:
            json_load = json.load(handle)
            first = json_load['RequiredPackages_apt']
            if first is not None:
                if json_load['RequiredPackages_apt']['all'] is None:
                    for x in first:
                        my_list.append(x)
                else:
                    for x in json_load['RequiredPackages_apt']['all']:
                        my_list.append(x)
        i += 1
    return(my_list)

#====================================================================
# Функции работы с xml
#====================================================================

# Функция проверки тега в xml

def get_tag_from_xml_file(path ,file_name, tag_name):

    if is_file(path, file_name) == False:
        return(False)

    tree = ET.parse(file_name)
    root = tree.getroot()

    # Находим все теги "book"
    for book in root.findall(tag_name):
        # Находим тег "title" и выводим его текст
        title = book.find('title').text
        return print(title)
    
# Функция преобразования xml -> html

def xml_to_html(xml_file) -> bool:
    pattern = "\d+"
    for file in xml_file:
        pattern = re.compile(pattern)
        x=re.findall(pattern,file)
        if x :
            xml=file
            html=x[0]+".html"
            subprocess.call(['xsltproc',xml,'-o',html])
    return(True)

#====================================================================
# Функция обратного отсчёта времени от текущего -1 минута
#====================================================================
def reverse_time() -> str:
    i = 0
    while True:
        time.sleep(60)
        now = datetime.datetime.now()
        delta = datetime.timedelta(minutes=i) 
        result = now - delta  
        i += 1
        return(result.strftime("%H:%M"))

#====================================================================
# Функция поточного запуска функции, тут вариант с stress-ng принтом что он работает
#====================================================================
def stressng_function() -> bool:
    def stress_test() -> bool:
        os.system("sudo script -c 'stress-ng --cpu 0 --cpu-method all -t 1h --metrics' > stress-ng.log")
        return(True)

    def status_message() -> bool:
        i = 1
        result = 60
        while True:
            if not thread1.is_alive():
                break
            time.sleep(60)
            if result == 0:
                return(True)
            result -= i
            print(result)

    thread1 = threading.Thread(target=stress_test)
    thread2 = threading.Thread(target=status_message)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    return(True)

#====================================================================
# Функция логирования трёх статусов в лог соответствующий наименованию модуля где был вызван
#====================================================================
import logging

def logger(msg, log_file, level=logging.INFO):
    log_file = os.path.splitext(os.path.basename(log_file))[0]
    log_file_msgformat = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    logging.basicConfig(filename=f'{log_file}.log',
                        filemode='a',
                        format=log_file_msgformat,
                        level=logging.INFO)

    if level == logging.INFO:
        logging.info(f'{log_file}: {msg}')
    elif level == logging.WARNING:
        logging.warning(f'{log_file}: {msg}')
    elif level == logging.ERROR:
        logging.error(f'{log_file}: {msg}')

