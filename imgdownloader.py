from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import chromedriver_autoinstaller
import os
import warnings
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps
import random
import shutil
from after_error import after_error
from getpass import getuser

user = getuser()
first_path = f'C:\\Users\\{user}\\Pictures'

warnings.filterwarnings("ignore")
chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

search = str(input('Search: '))

IU_Keywords = ['Iu', 'IU', '아이유', '안경유', 'iu', 'iU']

is_man = False
for i in range(len(IU_Keywords)):
    if IU_Keywords[i] in search:
        model = load_model('models/더 정확한 아이유.h5')
        model_name = '더 정확한 아이유.h5'
        is_man = True
if is_man == False:
    print('남자 신체면 1번\n여자 신체면 2번\n그냥 남자면 3번\n그냥 여자면 4번')
    Q_1 = int(input(''))
    if Q_1 == 1:
        is_man = True
        model = load_model('models/몸.h5')
        model_name = '몸.h5'
    elif Q_1 == 2:
        is_man = False
        model = load_model('models/몸.h5')
        model_name = '몸.h5'
    elif Q_1 == 3:
        is_man = True
        model = load_model('models/남녀.h5')
        model_name = '남녀.h5'
    elif Q_1 == 4:
        is_man = False
        model = load_model('models/남녀.h5')
        model_name = '남녀.h5'
    else:
        raise TypeError('잘못 입력하셨습니다.')

driver.get(f'https://www.google.co.kr/search?q={search}&tbm=isch')
os.system('cls')

if_dir = 0
try:
    os.mkdir(search)
    os.chdir(search)
    print(f'{search}폴더를 새롭게 만들었습니다!')
    if_dir = 0
except:
    new_dir = search + str(random.randint(0, 100000))
    os.mkdir(new_dir)
    os.chdir(new_dir)
    print(f'{search}폴더가 이미 있어 {new_dir}폴더를 새롭게 만들었습니다!')
    if_dir = 1

SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_elements_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 0
expected_count = len(images)
print(f"expected image pieces: {expected_count}")
for image in images:
    st_time = time.time()
    try:
        image.click()
        imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img').get_attribute("src")
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgUrl, str(count) + ".jpg")
        count = count + 1
    except:
        pass
    ed_time = time.time()
    if count == 1:
        cm_time = ed_time-st_time
    else:
        cm_time = cm_time + (ed_time - st_time)
    print(f'Downloading  -  {count} images...  남은 예상 시간  {(ed_time- st_time)*(expected_count-count): .5} sec  ', end='\r')
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
            # Replace this with the path to your image
            image = Image.open(f'{first_path}/{search}/{j}.jpg')
            #resize the image to a 224x224 with the same strategy as in TM2:
            #resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            #turn the image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            # Load the image into the array
            data[0] = normalized_image_array

            # run the inference
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
            print(f'{percentage:<10}  -  {complete_time: .5} sec')
        except:
            pass
    os.chdir('{first_path}')
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
driver.close()