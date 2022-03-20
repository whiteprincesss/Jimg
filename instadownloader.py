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
import logindata as ld
from getpass import getuser
from glob import glob

user = getuser()
first_path = f'C:\\Users\\{user}\\Pictures'
os.chdir(first_path)
try:
    os.mkdir('instagram')
except:
    pass
os.chdir('instagram')
ID = ld.data['ID']
PW = ld.data['PASSWORD']
baseUrl = 'https://www.instagram.com/'
plusUrl = input('검색할 계정를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

try:
    folder = plusUrl
    os.mkdir(folder)
except:
    folder = plusUrl+str(random.randint(0,10000))
    os.mkdir(folder)
os.chdir(folder)

def dwl(search):
    class NULLaccountError(Exception):
        def __init__(self):
            super().__init__('없는 계정입니다.')
    class NULLuploadError(Exception):
        def __init__(self):
            super().__init__('계정에 게시물이 없습니다.')
    plusUrl = search
    warnings.filterwarnings("ignore")
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(2)
    driver.find_element_by_css_selector("#loginForm > div > div:nth-child(1) > div > label > input").send_keys(ID)
    driver.find_element_by_css_selector("#loginForm > div > div:nth-child(2) > div > label > input").send_keys(PW)
    driver.find_element_by_css_selector("#loginForm > div > div:nth-child(3) > button > div").click()
    time.sleep(3)
    try:
        driver.find_element_by_css_selector("#react-root > section > main > div > div > div > section > div > button").click()
    except:
        driver.close()
        dwl(plusUrl)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html)

    try:
        count = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/div/span').text
        count = int(count.replace(',',''))
    except:
        raise NULLaccountError
    if count == 0:
        raise NULLuploadError

    imglist = []
    for i in range(0, round(count/60)):
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
        except:
            break
    print('downloade start')
    n = 0
    insta = soup.select('.v1Nh3.kIKUG._bz0w')
    for i in imglist:
        imgUrl = imglist[n]
        with urlopen(imgUrl) as f:
            with open(plusUrl + str(n) + '.jpg', 'wb') as h:
                img = f.read()
                h.write(img)
        n += 1
    if glob('*.*') == []:
        f = open('Why this folder is empty.txt', 'w')
        f.write('계정이 비공개로 추측 됩니다.')
        f.close()
dwl(plusUrl)