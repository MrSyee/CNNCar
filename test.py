import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

Car_data = np.load("data.npz");
raw_img = Car_data['image']
trainX = [] #images
for img in raw_img[0:100]:
    trainX.append(rgb2gray(img))
trainX = np.array(trainX) / 255
trainX = np.reshape(trainX, (trainX.shape[0], 96,128, 1))
trainy = Car_data['angle']/100
trainy = trainy[150].reshape(1,1)
print (trainX[0])
print (trainX.shape)
print (trainX[0].reshape(1,-1)) # 96 x 128 -> 1 x 12288
print (trainy)
