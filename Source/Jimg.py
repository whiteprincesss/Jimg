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
from getpass import getuser
from glob import glob
import re
from keras.models import load_model
from selenium.webdriver.common.by import By

user = getuser()
if not os.path.isfile('imgdown_setting.txt'):
    f = open('imgdown_setting.txt', 'w')
    f.write(f'C:\\Users\\{user}\\Pictures')
    f.close()
r = open('imgdown_setting.txt','r')
check_path = r.readline()
r.close()
first_path = check_path

warnings.filterwarnings("ignore")
chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

print('='*30)
search = input('Search: ')
IU_Keywords = ['Iu', 'IU', '아이유', '안경유', 'iu', 'iU']

def convert_time(time):
    time = float(time)
    hour = int(time//3600)
    left_time = round(time%3600, 2)
    min = int(left_time//60)
    sec = round(left_time%60, 2)
    return (hour, min, sec)
    
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

    radio = driver.find_element(By.XPATH, '//*[@id="regiontGA"]/div/span[1]')
    radio.click()
    save_icon = driver.find_element(By.XPATH, '//*[@id="form-buttons"]/div[1]')
    save_icon.click()

try:
    is_iu = False
    is_man = False
    is_woman = False
    for i in range(len(IU_Keywords)):
        if IU_Keywords[i] in search:
            model = load_model(f'models\아이유V2.h5')
            model_name = '아이유 ver.2'
            is_iu = True
            break
    if is_iu == False:
        while True:
            print('남자면 1번\n여자면 2번\n그 외의 것이면 3번')
            Q_1 = int(input(': '))
            if Q_1 == 1:
                if search[-1] == '&':
                    is_man = True
                    is_woman = False
                    model = load_model(r'models\몸V2.h5')
                    model_name = '몸 ver.2'
                    search = search[:-1]
                    break
                else:
                    is_man = True
                    is_woman = False
                    model = load_model(r'models\남녀.h5')
                    model_name = '남녀'
                    break
            elif Q_1 == 2:
                if search[-1] == '&':
                    is_man = False
                    is_woman = True
                    model = load_model(r'models\몸V2.h5')
                    model_name = '몸 ver.2'
                    search = search[:-1]
                    break
                else:
                    is_man = False
                    is_woman = True
                    model = load_model(r'models\남녀.h5')
                    model_name = '남녀'
                    break
            elif Q_1 == 3:
                is_man = False
                is_woman = False
                model = load_model(r'models\몸V2.h5')
                model_name = '몸 ver.2'
            else:
                raise TypeError('잘못 입력하셨습니다.')
    st_time = time.time()
    driver = webdriver.Chrome(options=options)
    if model_name == '몸 ver.2':
        change_location()
    driver.get(f'https://www.google.com/search?as_st=y&tbm=isch&hl=ko&as_q={search}&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:photo')

    if_dir = 0
    os.system('cls')
    try:
        os.chdir(first_path)
    except FileNotFoundError:
        print('********************************오류********************************')
        print('존재하지 않는 폴더입니다.\n기본 폴더로 설정을 변경합니다.')
        f = open('imgdown_setting.txt', 'w')
        f.write(f'C:\\Users\\{user}\\Pictures')
        first_path = f'C:\\Users\\{user}\\Pictures'
        f.close()
        os.chdir(first_path)
    global new_dir
    try:
        new_dir = search
        os.mkdir(new_dir)
        os.chdir(new_dir)
        print('================================================기본 정보================================================')
        print(f'{new_dir}폴더를 새롭게 만들었습니다!')
        print(f'{first_path}\{new_dir}')
        if is_iu == True:
            pass
        elif is_man == True:
            print('Selected Mode: 남자')
        elif is_woman == True:
            print('Selected Mode: 여자')
        else:
            print('Selected Mode: 기타')
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
                driver.find_elements(By.CSS_SELECTOR, ".mye4qd").click()
                print('Scroll')
            except:
                print('Scroll Finish')
                break
        last_height = new_height

    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    count = 0
    for image in images:
        try:
            image.click()
            imgUrl = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
            count = count + 1
        except:
            pass
        print('\033[38;2;99;247;249m' + f'다운로드 현황  {count:<5}개' + '\033[0m', end='\r')
    print('다운로드 완료!' + '\033[38;2;99;247;249m' + f'...{count}개 다운 완료' + '\033[0m')
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
                if len(prediction) == 2:
                    first_prediction = round(float(prediction[0])*100, 2)
                    second_prediction = round(float(prediction[1])*100, 2)
                else:
                    first_prediction = round(float(prediction[0])*100, 2)
                    second_prediction = round(float(prediction[1])*100, 2)
                    last_prediction = round(float(prediction[2])*100, 2)
                
                total_predictions = []
                total_predictions.append(first_prediction)
                total_predictions.append(second_prediction)
                if len(prediction) == 2:
                    pass
                else:
                    total_predictions.append(last_prediction)
                
                max_predictions = max(total_predictions)
                
                filename = '{}.jpg'.format(j)
                src = f'{first_path}/{search}/'
                if model_name == '남녀':
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
                # print(f'{percentage:<10}  -  {complete_time: .5} sec', end='\r')
            except ValueError:
                pass
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
        except:
            print('오류 발생!')
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
    print(f'\t\t\t\t\t')
    print("필터링 시작")
    filtered_count = 0
    for index, file_name in enumerate(os.listdir(search)):
        try:
            file_path = os.path.join(search, file_name)
            img = Image.open(file_path)
            # 이미지 해상도의 가로와 세로가 모두 350이하인 경우
            if img.width < 351 and img.height < 351:
                img.close()
                os.remove(file_path)
                filtered_count += 1
            else:
                img.close()
        # 이미지 파일이 깨져있는 경우
        except OSError:
            os.remove(file_path)
            filtered_count += 1
    print(f'삭제한 파일 개수: {filtered_count}개')
    os.chdir(search)
    filelist = []
    files = os.listdir()
    for i in range(len(files)):
        filelist.append(int(files[i].split('.')[0]))
    filelist.sort()
    for i in range(len(files)):
        os.rename(str(filelist[i])+'.jpg', f'{i}.jpg')
        final_num = i+1
    print(f'\t\t\t\t\t')
    print(f'완료!\n총 {final_num}개 다운 됨')
    ed_time = time.time()
    during_time = round(ed_time-st_time, 2)
    during_time = convert_time(during_time)
    print(f'총 시간: {during_time[0]}시간 {during_time[1]}분 {during_time[2]}초')
    driver.close()
except Exception as e:
    print(e)
    os.chdir(first_path)
    os.remove(new_dir)
    print('오류로 인해 작업을 취소합니다.')