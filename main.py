import subprocess
import os

import web
import soup
#I can do it better, but it's not necessary
realpath = os.path.realpath('..')
additional_path = 'tstu_bot'
SCHEDULE_DIRECTORY = 'schedule'
CONVERTED_DIRECTORY = 'converted_to_xml'
file_path = os.path.join(realpath , additional_path)

subprocess.call(os.path.join(file_path, "download_schedule"))
for (root,dirs,files) in os.walk(SCHEDULE_DIRECTORY): 
    for f in files:
        try:
            web.execute(os.path.join(file_path, SCHEDULE_DIRECTORY) , f)
        finally:
            print('Error: '+ f)

for (root,dirs,files) in os.walk(CONVERTED_DIRECTORY): 
    for f in files:
        objects = soup.execute(os.path.join(file_path, CONVERTED_DIRECTORY, f))
        for obj in objects:
            new_f = open(f.split('.')[0] + 'json', 'w')#TODO(Check implicit point)
            new_f.write(obj.toJSON())