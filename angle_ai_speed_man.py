import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/module')
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

from tensorClass import tensor
from cameraClass import Camera
from carClass import Car
from networkClass import Receiver


def main():

        car = Car()

        camera = Camera(car)
        camera.set_fps(30)
        
        receiver = Receiver()
        cnn = tensor()

        receiver.start()
        print("server start")

        
        while True:
                try:
                        
                        camera.capture_as_file()
                        
                        img = camera.capture()
                        
                        angle = cnn.run(img) * 100
                        speed = receiver.get_speed_angle()['speed']

                        if speed < 30:
                                speed = 0
                        else:
                                speed = 50
                        
                        car.set_speed_angle( speed, angle )

                        
                        
                except KeyboardInterrupt:

                        break


if __name__ == "__main__":
        main()
