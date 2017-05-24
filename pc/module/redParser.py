

import cv2
import numpy as np


def get_red_pixel_num(img_orig): #image = [48][128][3]

    img_orig = cv2.blur(img_orig, (3,3))
    hsv = cv2.cvtColor(img_orig, cv2.COLOR_HSV2RGB)

    lower1 = np.array([0, 0, 200])
    upper1 = np.array([30, 255, 255])

    lower2 = np.array([170, 0, 200])
    upper2 = np.array([180, 255, 255])    

    mask0 = cv2.inRange(hsv, lower1, upper1)
    mask1 = cv2.inRange(hsv, lower2, upper2)

    img_mask = mask0 + mask1
    cv2.imshow('red',img_mask)
    cv2.waitKey(1)

    not_zero = cv2.countNonZero(img_mask)
    return not_zero

    
