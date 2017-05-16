
import numpy as np
import math
import colorsys
import time
import cv2
import numpy as np


def get_red_pixel_num(img): #image = [48][128][3]


    c = time.time()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0, 150, 100])
    upper1 = np.array([15, 255, 255])

    lower2 = np.array([165, 150, 100])
    upper2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)

    mask = mask1+mask2

    not_zero = cv2.countNonZero(mask)
    return not_zero


