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

def googledownloader():
    search = input('Search: ')
    IU_Keywords = ['Iu', 'IU', '아이유', '안경유', 'iu', 'iU']

    is_man = False
    for i in range(len(IU_Keywords)):
        if IU_Keywords[i] in search:
            model = load_model('models/더 정확한 아이유.h5')
            model_name = '더 정확한 아이유.h5'
            is_man = True
            break
    if is_man == False:
        while True:
            print('남자 신체면 1번\n여자 신체면 2번\n그냥 남자면 3번\n그냥 여자면 4번')
            Q_1 = int(input(': '))
            if Q_1 == 1:
                is_man = True
                model = load_model('models/몸.h5')
                model_name = '몸.h5'
                break
            elif Q_1 == 2:
                is_man = False
                model = load_model('models/몸.h5')
                model_name = '몸.h5'
                break
            elif Q_1 == 3:
                is_man = True
                model = load_model('models/남녀.h5')
                model_name = '남녀.h5'
                break
            elif Q_1 == 4:
                is_man = False
                model = load_model('models/남녀.h5')
                model_name = '남녀.h5'
                break
            else:
                raise TypeError('잘못 입력하셨습니다.')
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.google.co.kr/search?q={search}&tbm=isch')

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
                
                filename = '{}.jpg'.format(j)
                src = f'{first_path}/{search}/'
                if is_man == True:
                    if first_prediction >= second_prediction:
                        dir = f'{first_path}/expected to {search}/'
                    else:
                        dir = f'{first_path}/expected not {search}/'
                else:
                    if first_prediction >= second_prediction:
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
    print('\t\t\t\t')
    print('Finish')
    driver.close()

def instadownlader():
    baseUrl = 'https://www.instagram.com/'
    plusUrl = input('검색할 계정를 입력하세요 : ')
    url = baseUrl + quote_plus(plusUrl)
    def dwl(search):
        try:
            class NULLaccountError(Exception):
                def __init__(self):
                    super().__init__('없는 계정입니다.')
            class NULLuploadError(Exception):
                def __init__(self):
                    super().__init__('계정에 게시물이 없습니다.')
            plusUrl = search

            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)
            try:
                driver.find_element_by_css_selector("#loginForm > div > div:nth-child(1) > div > label > input").send_keys(ID)
                driver.find_element_by_css_selector("#loginForm > div > div:nth-child(2) > div > label > input").send_keys(PW)
                driver.find_element_by_css_selector("#loginForm > div > div:nth-child(3) > button > div").click()
                time.sleep(3)
                try:
                    driver.find_element_by_css_selector("#react-root > section > main > div > div > div > section > div > button").click()
                except:
                    driver.close()
                time.sleep(3)
            except:
                pass

            html = driver.page_source
            soup = BeautifulSoup(html)

            try:
                count = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/div/span').text
                count = int(count.replace(',',''))
            except:
                raise NULLaccountError
            if count == 0:
                raise NULLuploadError
            try:
                name = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/span').text
            except:
                name = plusUrl
            try:
                name = name.split(' ')[0]
            except:
                pass
            reg = re.compile(r'[가-힣a-zA-Z]')
            if reg.match(name):
                name = name
            else:
                name = ''
            os.chdir(first_path)
            try:
                os.mkdir('instagram')
            except:
                pass
            os.chdir('instagram')
            folder = f'{str(name)}({plusUrl})'
            try:
                os.mkdir(folder)
            except:
                os.chdir(folder)
                f_l = glob('*.*')
                for i in range(len(f_l)):
                    os.remove(f_l[i])
                os.chdir('..')
                os.rmdir(folder)
                os.mkdir(folder)
            os.chdir(folder)
            
            imglist = []
            j = 1
            for i in range(0, round(count/6)):
                try:
                    insta = soup.select('.v1Nh3.kIKUG._bz0w')
                    for i in insta:
                        try:
                            imgUrl = i.select_one('.KL4Bh').img['src']
                            imglist.append(imgUrl)
                            imglist = list(set(imglist))
                            html = driver.page_source
                            soup = BeautifulSoup(html)
                            insta = soup.select('.v1Nh3.kIKUG._bz0w')
                        except:
                            break
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print(f'스크롤 중... try:{j}')
                    j += 1
                except:
                    break
            print('downloade start')
            n = 0
            insta = soup.select('.v1Nh3.kIKUG._bz0w')
            for i in imglist:
                imgUrl = imglist[n]
                with urlopen(imgUrl) as f:
                    with open(plusUrl +'-'+str(n) + '.jpg', 'wb') as h:
                        img = f.read()
                        h.write(img)
                print(f'downloading...  {str(round((n+1)/count*100 ,2))}%')
                n += 1
            print('download completed!')
            if glob('*.*') == []:
                os.chdir('..')
                os.rmdir(folder)
                print("비공개 계정인거 같아요!")
        except:
            dwl(plusUrl)
    dwl(plusUrl)

while True:
    print("""
    ========================Image Downloader========================
                    1. Download image in google
                    2. Download image in instagram
    ================================================================
        """)
    search_browser = input('Enter number: No.')
    if search_browser == '1':
        googledownloader()
        break
    elif search_browser == '2':
        instadownlader()
        break
    else:
        print('Try again')
    