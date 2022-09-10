from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import chromedriver_autoinstaller
import os
import warnings
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image, ImageOps
import random
import shutil
from after_error import after_error
from getpass import getuser
from glob import glob
import re
from keras.models import load_model

ld = open('logindata.txt','r')
data = ld.read().split(',')
ld.close()
reg = re.compile(r'[가-힣a-zA-Z]')
ID = data[0]
PW = data[1]
user = getuser()
first_path = f'C:\\Users\\{user}\\Pictures'

warnings.filterwarnings("ignore")
chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

print('='*30)
search = input('Search: ')
IU_Keywords = ['Iu', 'IU', '아이유', '안경유', 'iu', 'iU']

def change_location():
    driver.get(f'https://www.google.com/preferences')
    SCROLL_PAUSE_SEC = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    radio = driver.find_element_by_xpath('//*[@id="regiontGA"]/div/span[1]')
    radio.click()
    save_icon = driver.find_element_by_xpath('//*[@id="form-buttons"]/div[1]')
    save_icon.click()

is_iu = False
is_man = False
is_woman = False
for i in range(len(IU_Keywords)):
    if IU_Keywords[i] in search:
        model = load_model('models/더 정확한 아이유.h5')
        model_name = '더 정확한 아이유.h5'
        is_iu = True
        break
if is_man == False:
    while True:
        print('남자 신체면 1번\n여자 신체면 2번\n그냥 남자면 3번\n그냥 여자면 4번\n그 외의 것이면 5번')
        Q_1 = int(input(': '))
        if Q_1 == 1:
            is_man = True
            is_woman = False
            model = load_model('models/더 정확한 몸.h5')
            model_name = '몸.h5'
            break
        elif Q_1 == 2:
            is_man = False
            is_woman = True
            model = load_model('models/더 정확한 몸.h5')
            model_name = '몸.h5'
            break
        elif Q_1 == 3:
            is_man = True
            is_woman = False
            model = load_model('models/남녀.h5')
            model_name = '남녀.h5'
            break
        elif Q_1 == 4:
            is_man = False
            is_woman = True
            model = load_model('models/남녀.h5')
            model_name = '남녀.h5'
            break
        elif Q_1 == 5:
            is_man = False
            is_woman = False
            model = load_model('models/더 정확한 몸.h5')
        else:
            raise TypeError('잘못 입력하셨습니다.')
driver = webdriver.Chrome(options=options)
if model_name == '몸.h5':
    change_location()
driver.get(f'https://www.google.com/search?q={search}&tbm=isch')

if_dir = 0
os.system('cls')
os.chdir(first_path)
try:
    os.mkdir(search)
    os.chdir(search)
    print(f'{search}폴더를 새롭게 만들었습니다!')
    print(f'{first_path}/{search}')
    if_dir = 0
except:
    new_dir = search + '_' + str(random.randint(0, 100000))
    os.mkdir(new_dir)
    os.chdir(new_dir)
    print(f'{search}폴더가 이미 있어 {new_dir}폴더를 새롭게 만들었습니다!')
    print(f'{first_path}\{new_dir}')
    if_dir = 1
SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_elements_by_css_selector(".mye4qd").click()
            print('Scroll')
        except:
            print('Scroll Finish')
            break
    last_height = new_height

#법ㅎ
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 0
st_time = time.time()
for image in images:
    try:
        image.click()
        imgUrl = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
        count = count + 1
    except:
        pass
    print(f'Downloading  -  {count:<5} images...  ', end='\r')
ed_time = time.time()
cm_time = ed_time-st_time
print(f'Downloading was successful!  -  {cm_time: .5} sec  complete {count} images')
fincount = count
os.chdir(first_path)
if if_dir == 0:
    os.mkdir(f'expected to {search}')
    os.mkdir(f'expected not {search}')
else:
    search = new_dir
    os.mkdir(f'expected to {search}')
    os.mkdir(f'expected not {search}')
if is_iu == False:
    try:
        for j in range(fincount):
            try:
                start_time = time.time()
                data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                image = Image.open(f'{first_path}/{search}/{j}.jpg')
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)
                image_array = np.asarray(image)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                prediction = model.predict(data)
                prediction = str(prediction)[2:-2].split()
                first_prediction = round(float(prediction[0])*100, 2)
                second_prediction = round(float(prediction[1])*100, 2)
                last_prediction = round(float(prediction[2])*100, 2)
                
                total_predictions = []
                total_predictions.append(first_prediction)
                total_predictions.append(second_prediction)
                total_predictions.append(last_prediction)
                
                max_predictions = max(total_predictions)
                
                filename = '{}.jpg'.format(j)
                src = f'{first_path}/{search}/'
                if is_man == True:
                    if max_predictions == first_prediction:
                        dir = f'{first_path}/expected to {search}/'
                    else:
                        dir = f'{first_path}/expected not {search}/'
                elif is_woman == True:
                    if max_predictions == second_prediction:
                        dir = f'{first_path}/expected to {search}/'
                    else:
                        dir = f'{first_path}/expected not {search}/'
                else:
                    if max_predictions == last_prediction:
                        dir = f'{first_path}/expected not {search}/'
                    else:
                        dir = f'{first_path}/expected to {search}/'
                shutil.move(src+filename, dir+filename)
                end_time = time.time()
                global complete_time
                if j == 0:
                    complete_time = end_time-start_time
                else:
                    complete_time = complete_time + (end_time-start_time)
                percentage = str(round((j+1)/fincount*100, 2))
                if len(percentage.split('.')[1]) == 1:
                    percentage = percentage+'0%'
                else:
                    percentage = percentage + '%'
                print(f'{percentage:<10}  -  {complete_time: .5} sec', end='\r')
            except:
                pass
        os.chdir(search)
        search_files = glob('*.*')
        for i in range(len(search_files)):
            os.remove(search_files[i])
        os.chdir(first_path)
        os.rmdir(search)
        def rmodir(filePath):
            try:
                for file in os.scandir(filePath):
                    os.remove(file.path)
                os.rmdir(filePath)
            except:
                pass
        rmodir(f'expected not {search}')
        os.rename(f'expected to {search}', search)
        os.chdir(search)
        filelist = []
        files = os.listdir()
        for i in range(len(files)):
            filelist.append(int(files[i].split('.')[0]))
        filelist.sort()
        for i in range(len(files)):
            os.rename(str(filelist[i])+'.jpg', f'{i}.jpg')
    except:
        after_error(search, model_name, is_man)
elif is_iu == True:
    try:
        for j in range(fincount):
            try:
                start_time = time.time()
                data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                image = Image.open(f'{first_path}/{search}/{j}.jpg')
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)
                image_array = np.asarray(image)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                prediction = model.predict(data)
                prediction = str(prediction)[2:-2].split()
                first_prediction = round(float(prediction[0])*100, 2)
                second_prediction = round(float(prediction[1])*100, 2)
                
                total_predictions = []
                total_predictions.append(first_prediction)
                total_predictions.append(second_prediction)
                
                max_predictions = max(total_predictions)
                
                filename = '{}.jpg'.format(j)
                src = f'{first_path}/{search}/'
                if max_predictions == first_prediction:
                    dir = f'{first_path}/expected not {search}/'
                else:
                    dir = f'{first_path}/expected to {search}/'
                shutil.move(src+filename, dir+filename)
                end_time = time.time()
                if j == 0:
                    complete_time = end_time-start_time
                else:
                    complete_time = complete_time + (end_time-start_time)
                percentage = str(round((j+1)/fincount*100, 2))
                if len(percentage.split('.')[1]) == 1:
                    percentage = percentage+'0%'
                else:
                    percentage = percentage + '%'
                print(f'{percentage:<10}  -  {complete_time: .5} sec', end='\r')
            except:
                pass
        os.chdir(search)
        search_files = glob('*.*')
        for i in range(len(search_files)):
            os.remove(search_files[i])
        os.chdir(first_path)
        os.rmdir(search)
        def rmodir(filePath):
            try:
                for file in os.scandir(filePath):
                    os.remove(file.path)
                os.rmdir(filePath)
            except:
                pass
        rmodir(f'expected not {search}')
        os.rename(f'expected to {search}', search)
        os.chdir(search)
        filelist = []
        files = os.listdir()
        for i in range(len(files)):
            filelist.append(int(files[i].split('.')[0]))
        filelist.sort()
        for i in range(len(files)):
            os.rename(str(filelist[i])+'.jpg', f'{i}.jpg')
    except:
        after_error(search, model_name, is_man)
print('\t\t\t\t')
print('Finish')
driver.close()
    