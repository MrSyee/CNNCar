#-*- coding:utf-8 -*-

import sys
import time
import pickle
import cv2
import numpy as np

from module.haarClass import Haar
from module.networkClass import Network
from module.tensorClass import Tensor
from module.templateClass import Template
import module.redParser as red

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8000

data = {'speed': 30, 'angle': 50}
speed = 0
angle = 0

network = Network('192.168.255.181', port)
sess = Tensor()
body_finder = Haar(1.1  , "haarcascade_fullbody.xml")

stop_time = 0


def main_process():
    global stop_time

    while True:

        raw = network.recv()

        if raw == -1:
            network.send(pickle.dumps(data))
            continue

        img = cv2.imdecode(np.fromstring(raw, dtype=np.uint8), cv2.IMREAD_COLOR)

        if 'T' in dir(img):

            angle = sess.run(img) * 100

            cv2.imshow("img",img)
            cv2.waitKey(1)

            if red.get_red_pixel_num(img) > 1 or body_finder.classify(img):
                stop_time = time.time()
                speed = 0
            elif time.time() - stop_time < 3.0:
                speed = 0
            else:
                speed = 40

        else:
            angle = 50
            speed = 0

        data['speed'] = speed
        data['angle'] = angle

        network.send( pickle.dumps(data) )

if __name__ == '__main__':

    try:
        main_process()

    except KeyboardInterrupt:
        print(" [*] calculator stop")

    except BaseException as error:
        print("\n [E] cal.py {}".format(error.args))
