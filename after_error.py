import os
import time
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps
import shutil
from getpass import getuser
from glob import glob

model_path = os.getcwd()
user = getuser()
first_path = f'C:\\Users\\{user}\\Pictures'

def after_error(search, model_name, is_man):
    model = load_model(f'{model_path}/models/{model_name}')
    os.chdir(first_path)
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
            if j == int(filelists[1]):
                complete_time = end_time-start_time
            else:
                complete_time = complete_time + (end_time-start_time)
            j += 1
        except:
            pass
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
    return 'Done'