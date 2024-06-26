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
import xmltodict
import functools
import hashlib

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

# Функции проверки спика каталогов и вложенных файлов файлов
def get_files_list(dir_path):
  file_list = []

  for root, dirs, files in os.walk(dir_path):
    for file in files:
      file_list.append(os.path.join(root, file))

  return file_list

# Функция рекурсивного копирования файлов из одной дирректории в другую
import shutil
def copy_files_to_RFAL():
    src_dir = os.getcwd()
    dest_dir = "/RFAL"

    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        src = os.path.join(src_dir, item)
        dest = os.path.join(dest_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dest, False, None)
        else:
            shutil.copy2(src, dest)
    return(True)

# ============================================================================
# Скрипт для глобального переименования файлов в дирректории
# ============================================================================
from os import listdir
from os.path import isfile, join
import os

def rename_in_dir() -> bool:
    onlyfiles = [f for f in listdir(os.path.abspath(os.curdir)) if isfile(join(os.path.abspath(os.curdir), f))]
    for i in onlyfiles:
        print(i)
        if i[:3].upper().lower() == 'Cer'.upper().lower():
            b = i.split('_')
            if b[1][:2].upper().lower() == 'se'.upper().lower():
                os.rename(i, f'Certificate_alse_{b[2]}')
                print(f'{i} переименован в - Certificate_alse_{b[2]}')
    return(True)

# проверку можно осуществить следующим примером
#if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,get_files_list('/boot'),get_files_list('/home')), True):
#     print (f"The lists first_list and second_list are the same")
#else:
#    print (f"The lists first_list and second_list are not the same")


# ============================================================================
# Функции поиска, подтверждения и записи в файлах
# ============================================================================
# Функция снятия MD5
def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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

# Функция преобразования lshw.xml -> json
def lshw_to_json():
    result = subprocess.run(['lshw', '-xml'], stdout=subprocess.PIPE)
    xml_output = result.stdout

    json_output = json.dumps(xmltodict.parse(xml_output), indent=4, sort_keys=True)

    return(json_output)

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


# ============================================================================
# Логер передаётся через __file__ в .log
# ============================================================================
def logger_log(module_name):
    log_file = os.path.splitext(os.path.basename(module_name))[0]
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)

    if not os.path.isdir(f'/RFAL/{os.uname().release}/other_logs'):
        os.makedirs(f'/RFAL/{os.uname().release}/other_logs')

    handler = logging.FileHandler(f'/RFAL/{os.uname().release}/other_logs/{log_file}.log')
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s: %(lineno)d - %(message)s')
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger

# ============================================================================
# Логер передаётся через __file__ в console
# ============================================================================

def logger_console(module_name, type, msg):
    RESET = "\033[0m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    BLUE = "\e[0;34m"

    TYPE = {
        'error' or 'ERROR' : f'{RED} ERROR {RESET}',
        'crytical' and 'CRYTICAL' : f'{RED} CRYTICAL {RESET}',
        'info' and 'INFO' : f'{GREEN} INFO {RESET}',
        'blue' and 'DEBUG' : f'{BLUE} DEBUG {RESET}',
        'warning' and 'WARNING' : f'{YELLOW} WARNING {RESET}'
    }

    print (f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {os.path.splitext(os.path.basename(module_name))[0]} - {TYPE[type]} - {msg}')

#logger_main = logger_module.get_logger(__file__)
#logger_main.info('This is an info message')
#logger_main.warning('This is a warning message')
#logger_main.error('This is an error message')

# ============================================================================
# Функция отслеживания изменений в указанной дирректории или файле
# ============================================================================
import pyinotify
import signal


logger = sys_logger.logger_log(__file__)
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        logger_console(__file__, 'error', f"Creating:{event.pathname}")

    def process_IN_DELETE(self, event):
        logger_console(__file__, 'error', f"Removing:{event.pathname}")

    def process_IN_MODIFY(self, event):
        logger_console(__file__, 'error', f"Modifying:{event.pathname}")

    def process_IN_ATTRIB(self, event):
        logger_console(__file__, 'error', f"Changing attribute:{event.pathname}")

    def process_IN_MOVED_FROM(self, event):
        logger_console(__file__, 'error', f"Moving out:{event.pathname}")

def exit_gracefully(signum, frame):
    logger_console(__file__, 'info', f"Monitoring stop")
    sys.exit()

def monitor_changes(directory='/'):
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_ATTRIB | pyinotify.IN_MOVED_FROM

    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)

    wm.add_watch(directory, mask)

    try:
        logger_console(__file__, 'info', f"Monitoring start")
        notifier.loop()
    except KeyboardInterrupt:
        logger_console(__file__, 'info', f"Monitoring stop")
        notifier.stop()

# ============================================================================
# Функция создания systemd
# ============================================================================
def init_func(name, path) -> bool:
    logger.info(f"start: init_func()")
    service_content = f'[Unit]\nDescription={name}\n\n[Service]\nExecStart={path}{name} start\nExecStop={path}{name} stop\n\n[Install]\nWantedBy=multi-user.target'
    with open('/etc/systemd/system/{name}.service', 'w') as f:
        f.write(service_content)
    time.sleep(1)
    os.system('sudo systemctl daemon-reload')
    time.sleep(1)
    return(True)

# ============================================================================
# Функция прерывания
# ============================================================================

# Функция kill процесса по имени и пиду

def kill_pid(name_pid):
    print("stop mode")
    name = os.popen('sudo pgrep -f {name_pid}').read().rstrip().split('\n')
    os.system(f'sudo kill {name[0]}')

# Функция обработки прерывания ctrl+c

import signal
#signal.signal(signal.SIGTERM, exit_gracefully)
#signal.signal(signal.SIGINT, exit_gracefully)



# ============================================================================
# Функция быстрой сортировки
# ============================================================================
def quiksort(array):
    if len(array) < 2:
        return array
    pivot = array[0]
    less = [i for i in array[1:] if i < pivot]
    greater = [i for i in array[1:] if i > pivot]
    return quiksort(less) + [pivot] + quiksort(greater)
    

# ============================================================================
# БЫстрая сортировка с применением  алгоритма Лемпера-Тарьяна
# ============================================================================
def median_of_three(array, start, end):
    mid = (start + end) // 2
    if array[start] < array[mid]:
        if array[mid] < array[end]:
            return mid
        elif array[start] < array[end]:
            return end
        else:
            return start
    elif array[start] > array[end]:
        return end
    else:
        if array[mid] < array[end]:
            return end
        else:
            return mid

def partition(array, start, end):
    pivot_index = median_of_three(array, start, end)
    pivot = array[pivot_index]
    array[pivot_index], array[end] = array[end], array[pivot_index]
    i = start
    for j in range(start, end):
        if array[j] < pivot:
            array[i], array[j] = array[j], array[i]
            i += 1
    array[i], array[end] = array[end], array[i]
    return i


def quiksort(array, start=0, end=None):
    if end is None:
        end = len(array) - 1
    if start < end:
        pivot_index = partition(array, start, end)
        quiksort(array, start, pivot_index - 1)
        quiksort(array, pivot_index + 1, end)
    return array

# ============================================================================
# Поиск в ширину
# ============================================================================

from collections import deque

def bfs(graph, start_vertex):
    visited = set()
    queue = deque([start_vertex])

    while queue:
        vertex = queue.popleft()

        if vertex not in visited:
            visited.add(vertex)
            print(vertex)

            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

#bfs(graph, 'D')


# ============================================================================
# Алгоритм Беллмана-Форда для поиска кратчайшего пути с обработкой отрицательных весов
# ============================================================================

def bellman_ford(graph, source):
    distances = {vertex: float('inf') for vertex in graph}
    distances[source] = 0
    predecessors = {vertex: None for vertex in graph}

    for _ in range(len(graph) - 1):
        for vertex, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                if distances[vertex] + weight < distances[neighbor]:
                    distances[neighbor] = distances[vertex] + weight
                    predecessors[neighbor] = vertex

    # Проверка на отрицательные циклы
    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if distances[vertex] + weight < distances[neighbor]:
                return None, "Graph contains a negative cycle"

    return distances, predecessors


graph = {
    'A': {'B': 3, 'C': 4},
    'B': {'D': 2, 'E': -2},  # изменили вес ребра между вершинами B и E на -2
    'C': {'F': 2},
    'D': {'E': 1},
    'E': {'F': 1},
    'F': {}
}

#distances, predecessors = bellman_ford(graph, 'A')
#print("Distances:", distances)
#print("Predecessors:", predecessors)
