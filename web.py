from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""

def drag_and_drop_file(drop_target, path):
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)


def execute(file_path , file_name):
    WEBSITE_NAME = 'https://anyconv.com/ru/konverter-doc-v-xml/'

    realpath = os.path.realpath('..')
    folder_name = 'tstu_bot'
    driver_name = 'chromedriver'

    driver_path = os.path.join(realpath ,folder_name , driver_name)


    chrome_options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": os.path.join(realpath, folder_name,'converted_to_xml') ,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True }
    chrome_options.add_experimental_option("prefs", preferences)
    file_location = os.path.join(file_path, file_name)
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
    driver.get(WEBSITE_NAME)
    drop_area = driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div/div[1]/div/div[1]/p')

    drag_and_drop_file(drop_area , file_location)
    driver.implicitly_wait(60)
    convert_button = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/p/button')
    convert_button.click()
    driver.implicitly_wait(60)
    get_file_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div/div[1]/div/div[1]/div/div[3]/a')
    get_file_button.click()
    time.sleep(30)
    driver.close()