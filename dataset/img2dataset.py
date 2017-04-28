import numpy as np
import glob
import os
from scipy.misc import imread, imresize, imshow
import matplotlib.pyplot as plt


# 이미지 파일의 이름을 분리해서 저장.
cwd = os.getcwd()
imgsize = [96, 128]

file_list = glob.glob(cwd + '/image/*.jpg')
speed = [] # output data (speed, angle ...)
angle = []
img = [] # input data (image)


file_name = "data.npz"

# 폴더안의 모든 image파일 이름에서 정보 추출하고 gray scale로 변환
for file in file_list:
    file_path = file
    currimg =  imread(file_path)
    file = os.path.basename(file)
    file_ = os.path.splitext(file)[0]
    _, s, a = file_.split('_')
    speed.append(int(s))
    angle.append(int(a))
    currimg = currimg[48:96]
    img.append(currimg)


print (len(speed))
print(len(angle))
np.savez(file_name, image = img, speed = speed, angle = angle, dtype='int')

Car_data = np.load('data.npz')
raw_img = Car_data['image']
trainy = Car_data['angle']
print ("------------------------------")
print (raw_img.shape)
print (trainy)
print (trainy.shape)
