
import numpy as np
import math
import colorsys
import time
import cv2
import numpy as np


def get_red_pixel_num(img): #image = [48][128][3]


    #try:
    hsv = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

    lower1 = np.array([5, 0, 200])
    upper1 = np.array([40, 255, 255])

    lower2 = np.array([170, 0, 200])
    upper2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)

    mask = mask1+mask2
    img = cv2.resize(img, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
    cv2.imshow("img", img)
    cv2.waitKey(1)
    mask_tmp = cv2.resize(mask, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
    cv2.imshow("img_red",mask_tmp)
    cv2.waitKey(1)
    #print("\nred=%d"%cv2.countNonZero(mask))

    not_zero = cv2.countNonZero(mask)
    #except BaseException as e:
    #    print("\n [E] RED PARSER {}".format(e.args))
    #    return 0
    return not_zero
