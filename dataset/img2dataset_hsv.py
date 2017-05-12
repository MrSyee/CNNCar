import numpy as np
import glob
import os
from scipy.misc import imread, imresize, imshow, imsave
import matplotlib.pyplot as plt
import math

# RGB to HSV function
here_list = []
def img2hsv(img): #image = [48][128][3]
    here = 0
    for i in range(48):
        for k in range(128):
            c = img[i][k]

            h,s,v = rgb2hsv(c[0],c[1],c[2])

            #if (h<30 or h>330) and s>0.4 and v>0.2:
            if (h<30 or h>330 and h>=0 and h<=360) and s>0.4 and v>0.2:
                print("here!")
                here += 1
                continue
            else:
                img[i][k][0] = 0
                img[i][k][1] = 0
                img[i][k][2] = 0
    here_list.append(here)
    return img
total_v = []
total_s = []
total_h = []
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    total_s.append(s)
    total_h.append(h)
    v = mx

    total_v.append(v)
    return h, s, v

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

    n_img = img2hsv(currimg)
    n_img = rgb2gray(n_img)


    imsave('.\\hsv\\%s'%file,n_img)
    print ('.\\hsv\\%s'%file)
    img.append(n_img)

print (len(speed))
print(len(angle))
np.savez(file_name, image = img, speed = speed, angle = angle, dtype='int')


f = open("data.csv","w")
for i in range(len(speed)):
    f.write("{},{}\n".format(here_list[i],speed[i]))
f.close()



Car_data = np.load('data.npz')
raw_img = Car_data['image']
trainy = Car_data['angle']
print ("------------------------------")
print (raw_img.shape)
print (trainy)
print (trainy.shape)

print("h min {} max {}".format(min(total_h),max(total_h)))
print("s min {} max {}".format(min(total_s),max(total_s)))
print("v min {} max {}".format(min(total_v),max(total_v)))
