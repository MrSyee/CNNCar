
import numpy as np
import picamera

import os
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

class Camera():
        def __init__(self, car_object):

                WIDTH = 128
                HEIGHT = 96

                self.car = car_object
                self.cam = picamera.PiCamera()
                self.cam.resolution = (WIDTH,HEIGHT)

                self.cam.rotation = 180
                self.cam.framerate = 30

                self.out =  np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)


                if not os.path.exists(CUR_DIR+'/image'):
                        os.makedirs(CUR_DIR+'/image')
                self.image_index = 0
                while True:
                        if os.path.exists( CUR_DIR+"/image/%08d*.jpg"%(self.image_index) ):
                                self.image_index += 1
                        else:
                                break

        def capture(self):
                self.cam.capture(self.out, 'rgb', use_video_port = True)
                return np.array( self.out )


        def capture_as_file(self):
                self.cam.capture("image/%08d_%d_%d.jpg"%(self.image_index, self.car.get_speed(), self.car.get_normal_angle() ),
                                 'jpeg',
                                 use_video_port = True
                                 )
                self.image_index += 1
                
        def set_fps(self,fps):
                self.cam.framerate = fps
