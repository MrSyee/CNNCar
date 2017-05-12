import numpy as np
import glob
import os
from scipy.misc import imread, imresize, imshow, imsave
import matplotlib.pyplot as plt

# RGB to Gray function
def rgb2gray(rgb):
    if len(rgb.shape) is 3:
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    else:
        print ("Current Image if GRAY!")
        return rgb

# 이미지 파일의 이름을 분리해서 저장.
cwd = os.getcwd()
imgsize = [96, 128]

file_list = glob.glob(cwd + '/image_old5/*.jpg')
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
    grayimg = np.dot(currimg[...,:3], [0.299, 0.587, 0.114])
    imsave('.\\gray\\%s'%file,grayimg)
    print ('.\\gray\\%s'%file)
    img.append(grayimg)


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
