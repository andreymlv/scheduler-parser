import subprocess
import os

import web
import soup
#I can do it better, but it's not necessary
realpath = os.path.realpath('..')
additional_path = 'tstu_bot'
SCHEDULE_DIRECTORY = 'schedule'
CONVERTED_DIRECTORY = 'converted_to_xml'
MAX_NUMBER_OF_ATTEMPTS = 2
file_path = os.path.join(realpath , additional_path)

subprocess.call(os.path.join(file_path, "download_schedule"))
for (root,dirs,files) in os.walk(SCHEDULE_DIRECTORY): 
    for f in files:
        flag = False
        number_of_attempts = 0
        while flag == False:
            if number_of_attempts > MAX_NUMBER_OF_ATTEMPTS:
                print('File conversion error: '+ f)
                break
            number_of_attempts += 1
            flag = web.execute(os.path.join(file_path, SCHEDULE_DIRECTORY) , f)

for (root,dirs,files) in os.walk(CONVERTED_DIRECTORY): 
    for f in files:
        try:
            objects = soup.execute(os.path.join(file_path, CONVERTED_DIRECTORY, f))
        except Exception:
            print('File processing error: '+ f)
            continue
        for obj in objects:
            new_f = open(f.split('.')[0] + 'json', 'w')#TODO(Check implicit point)
            new_f.write(obj.toJSON())