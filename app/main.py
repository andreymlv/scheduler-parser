import subprocess
import os

import web
import soup

from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing

#I can do it better, but it's not necessary
realpath = os.path.realpath('..')
additional_path = os.path.join('app')
SCHEDULE_DIRECTORY = 'schedule'
CONVERTED_DIRECTORY = 'converted_to_xml'
FINAL_DIRECTORY = 'converted_to_json'
MAX_NUMBER_OF_ATTEMPTS = 1
file_path = os.path.join(realpath , additional_path)
CPU_COUNT = multiprocessing.cpu_count()

#Set this
semester = '1'
year = '2020-21'

def download_resources():
    subprocess.call([os.path.join(file_path, "download_schedule"), semester, year])

def convert_file_to_xml(f):
    flag = False
    number_of_attempts = 0
    while flag == False:
        if number_of_attempts > MAX_NUMBER_OF_ATTEMPTS:
            print('File conversion error: '+ f)
            break
        number_of_attempts += 1
        flag = web.execute(os.path.join(file_path, SCHEDULE_DIRECTORY) , f)   

def convert_all_to_xml():
    pool = ThreadPool(CPU_COUNT // 2)

    for (_,_,files) in os.walk(SCHEDULE_DIRECTORY): 
        pool.map(convert_file_to_xml,files)
    pool.close()
    pool.join()

def handle_files_and_save():
    for (_,_,files) in os.walk(CONVERTED_DIRECTORY): 
        for f in files:
            try:
                objects = soup.execute(os.path.join(file_path, CONVERTED_DIRECTORY, f))
            except Exception:
                print('File processing error: '+ f)
                continue
            for obj in objects:
                #index 1 in open is a potential vulnerability
                try:
                    if obj.name == '':
                        continue
                    json_path = os.path.join(file_path, FINAL_DIRECTORY , obj.name + '.json')
                    new_f = open(json_path, 'w')#TODO(Check implicit point)
                    new_f.write(obj.toJSON())
                    new_f.close()
                except Exception:
                    print('File conversion error')
                
download_resources()
convert_all_to_xml()
handle_files_and_save()