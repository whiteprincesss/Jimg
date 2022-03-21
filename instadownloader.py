from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import chromedriver_autoinstaller
import os
import requests
import warnings
import random
from getpass import getuser
from glob import glob
import subprocess
import shutil
import re

ld = open('logindata.txt','r')
data = ld.read().split(',')
ld.close()
reg = re.compile(r'[가-힣a-zA-Z]')

warnings.filterwarnings("ignore")

chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options=options

user = getuser()
first_path = f'C:\\Users\\{user}\\Pictures'
ID = data[0]
PW = data[1]
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
        try:
            folder = f'{str(name)}({plusUrl})'
            os.mkdir(folder)
        except:
            folder = f'{str(name)}({plusUrl})'+str(random.randint(0,10000))
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
            f = open('Why this folder is empty.txt', 'w')
            f.write('계정이 비공개로 추측 됩니다.')
            f.close()
    except:
        dwl(plusUrl)
dwl(plusUrl)