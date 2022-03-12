import os
import time
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps
import shutil

def after_error(search):
    IU_Keywords = ['Iu', 'IU', '아이유', '안경유', 'iu', 'iU']
    print('오류 후 기본 정보를 재수집합니다.')
    is_iu = False
    for i in range(len(IU_Keywords)):
        if IU_Keywords[i] in search:
            model = load_model('models/더 정확한 아이유.h5')
            is_iu = True
    is_man = False
    if is_iu == False:
        model = load_model('models/남녀.h5')
        print('남자면 1번, 여자면 2번')
        Q = int(input(''))
        if Q == 1:
            is_man = True
        elif Q == 2:
            is_man = False
        else:
            raise TypeError('잘못 입력하셨습니다.')
    filelists = []
    filess = os.listdir(f'{search}/')
    for i in range(len(filess)):
        filelists.append(filess[i].split('.')[0])
    filelists.sort()
    j = int(filelists[2])
    os.remove(f'{search}/{str(filelists[0])}.jpg')
    os.remove(f'{search}/{str(filelists[1])}.jpg')
    fincount=len(os.listdir(f'{search}/'))
    for k in range(fincount):
        start_time = time.time()
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        image = Image.open(f'python projects/{search}/{j}.jpg')
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
        src = f'python projects/{search}/'
        if is_iu == True:
            if first_prediction >= second_prediction:
                dir = f'python projects/expected to {search}/'
            else:
                dir = f'python projects/expected not {search}/'
        else:
            if is_man == True:
                if first_prediction >= second_prediction:
                    dir = f'python projects/expected to {search}/'
                else:
                    dir = f'python projects/expected not {search}/'
            else:
                if first_prediction >= second_prediction:
                    dir = f'python projects/expected not {search}/'
                else:
                    dir = f'python projects/expected to {search}/'
        shutil.move(src+filename, dir+filename)
        end_time = time.time()
        if j == int(filelists[1]):
            complete_time = end_time-start_time
        else:
            complete_time = complete_time + (end_time-start_time)
        print(f'{round((k+1)/fincount*100, 2)}%  -  {complete_time: .5} sec')
        j += 1
    os.chdir('python projects')
    try:
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
        pass
    return 'Done'