import subprocess
import os

import web
import soup
#I can do it better, but it's not necessary
realpath = os.path.realpath('..')
additional_path = 'tstu_bot'
SCHEDULE_DIRECTORY = 'schedule'
CONVERTED_DIRECTORY = 'converted_to_xml'
FINAL_DIRECTORY = 'converted_to_json'
MAX_NUMBER_OF_ATTEMPTS = 1
file_path = os.path.join(realpath , additional_path)

def download_resources():
    subprocess.call(os.path.join(file_path, "download_schedule"))

def convert_to_xml():
    for (_,_,files) in os.walk(SCHEDULE_DIRECTORY): 
        for f in files:
            flag = False
            number_of_attempts = 0
            while flag == False:
                if number_of_attempts > MAX_NUMBER_OF_ATTEMPTS:
                    print('File conversion error: '+ f)
                    break
                number_of_attempts += 1
                flag = web.execute(os.path.join(file_path, SCHEDULE_DIRECTORY) , f)

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
                json_path = os.path.join(file_path, FINAL_DIRECTORY , obj.name + '.json')
                new_f = open(json_path, 'w')#TODO(Check implicit point)
                new_f.write(obj.toJSON())
                new_f.close()

handle_files_and_save()