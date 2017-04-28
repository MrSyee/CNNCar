
# Car control by itself using CNN

import RPi.GPIO as GPIO
import picamera
import math


import tensorflow as tf
import numpy as np
import model
import model_op
import time
import sys
import os
CUR_DIR = os.path.dirname(os.path.abspath(__file__))



class tensor():
        def __init__(self):
                self.batch_size = 10
                self.input_height = 96
                self.input_width = 128
                self.input_channel = 1
                self.conv_1st_filter_n = 16
                self.conv_2nd_filter_n = 32

                self.checkpoint_dir = './checkpoint'
                self.model_name = "{}_{}_{}_{}".format('CNN_Car', self.batch_size, self.input_height, self.input_width)

                self.image = tf.placeholder(tf.float32, [self.batch_size, self.input_height, self.input_width, self.input_channel], name = 'image')
                self.logit = model._net(image, self.batch_size, self.conv_1st_filter_n, self.conv_2nd_filter_n)
                self.saver = tf.train.Saver()
                self.sess = tf.Session()
                self.sess.run(tf.global_variables_initializer())
                
                model_op.model_load(self.checkpoint_dir, self.model_name, self.sess, self.saver)

                print( "[ * ]: tensorflow loading finish")
                pass

        def get_tran(self, x):
                x = np.dot(x[...,:3],[0.299,0.587,0.114])
                x = np.array(x)/255
                x = np.reshape(x, (1, 96, 128, 1))
                return x

        def run(self, img):
                value = self.sess.run( out_label, feed_dict = {image : get_tran(img)} )
                return value[0][0]

class Camera():
        def __init__(self, car_object):

                WIDTH = 128
                HEIGHT = 96

                self.car = car_object
                self.cam = picamera.PiCamera()
                self.cam.resolution = (WIDTH,HEIGHT)

                self.cam.rotation = 180
                self.cam.framerate = 30

                self.saver = DataSet()
                self.out =  np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)


        def capture(self):
                self.cam.capture(self.out, 'rgb', use_video_port = True)
                return np.array( self.out )

        def set_fps(self,fps):
                self.cam.framerate = fps

class Car():
        def __init__(self):
                GPIO.setmode(GPIO.BCM)

                self.motor_pin = 23
                self.motor_in1_pin = 17
                self.motor_in2_pin = 27
                self.servo_pin = 21

                GPIO.setup(self.motor_pin, GPIO.OUT)
                GPIO.setup(self.motor_in1_pin, GPIO.OUT)
                GPIO.setup(self.motor_in2_pin, GPIO.OUT)
                GPIO.setup(self.servo_pin, GPIO.OUT)

                self.dc_motor = GPIO.PWM(self.motor_pin, 100)
                self.dc_motor.start(0)

                self.servo_motor = GPIO.PWM(self.servo_pin, 50)
                self.servo_motor.start(0)

                self.speed = 0
                self.angle = 76

        def __del__(self):
                GPIO.cleanup()

        # DC motor control
        def set_speed(self, val):

                if abs(val) > 100:
                        val = val/abs(val) * 100

                if(val>=0):
                        self.dc_motor.ChangeDutyCycle(val)
                        GPIO.output(self.motor_in1_pin, True)
                        GPIO.output(self.motor_in2_pin, False)
                else:
                        self.dc_motor.ChangeDutyCycle(100+val)
                        GPIO.output(self.motor_in1_pin, False)
                        GPIO.output(self.motor_in2_pin, True)
                self.speed = abs(val)

        # Servo motor control
        def set_angle(self, val):
                self.angle = val
                self.servo_motor.ChangeDutyCycle(val*0.1)

        def speed_str(self):
                return str(self.speed)
        def angle_str(self):
                return str(self.angle)
        def get_speed(self):
                return self.speed
        def get_angle(self):
                return self.angle
        def get_normal_angle(self):
                return 2*(self.angle-51)

        def set_speed_angle(self, raw_speed, raw_angle):
                angle = 51 + ( (101 - 51) * raw_angle/100.0 )

                # raw_angle [0,100] => angle [-45, 45] (degree) 매핑
                # angle [-45, 45] => [-0.7853, 0.7853] (radian) 매핑

                speed_a = (raw_angle-50)/50*45*3.141592/180


                #if speed_a < 0:
                #        speed_a = speed_a * 1.1
                speed_a = speed_a * 1.1

                speed = 1
                if raw_speed > 0:
                        speed = raw_speed/math.cos(speed_a)
                else:
                        speed = raw_speed
                self.set_speed(speed)
                self.set_angle(angle)



def main():

        car = Car()

        camera = Camera(car)
        camera.set_fps(30)

        cnn = tensor()

        
        while True:
                try:
                        img = camera.capture()
                        angle = cnn.run(img) * 100

                        car.set_speed_angle( 60, angle )

                except KeyboardInterrupt:

                        break


if __name__ == "__main__":
        main()
