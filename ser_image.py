
# Car control with smart phone

# -*- encoding:cp949 -*-

import RPi.GPIO as GPIO
import time
import socket
import threading
import os
import picamera
import math
import numpy as np

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER_DOWN = False


class DataSet():
        def __init__(self):
                self.image = []
                self.speed = []
                self.angle = []
                self.data_dir = CUR_DIR+"/data"

                if not os.path.exists(self.data_dir):
                        os.makedirs(self.data_dir)

        def save_data(self,image,speed,angle):
                self.image.append(image)
                self.speed.append(speed)
                self.angle.append(angle)

        def __del__(self):
                i = 0
                while True:
                        if os.path.exists(self.data_dir + "/save%02d.npz"%(i) ):
                                i = i + 1
                        else:
                                break
                length = [ len(self.image), len(self.speed), len(self.angle) ]
                length.sort()
                print(length)

                if length[0] != len(self.image):
                        self.image = self.image[:length[0]]
                if length[0] != len(self.speed):
                        self.speed = self.speed[:length[0]]
                if length[0] != len(self.angle):
                        self.angle = self.angle[:length[0]]


                np.savez(self.data_dir + "/save%02d.npz"%(i), image=self.image, speed=self.speed, angle=self.angle )
                print("data saved")

class Camera():
        def __init__(self, car_object):

                WIDTH = 128
                HEIGHT = 96

                self.car = car_object
                self.cam = picamera.PiCamera()
                self.cam.resolution = (WIDTH,HEIGHT)

                self.cam.rotation = 180
                self.cam.framerate = 30

                #self.saver = DataSet()
                self.out =  np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)
                self.image_index = 0

                # 00000001_speed_angle.jpg

                while True:
                        if os.path.exists( CUR_DIR+"/image/%08d*.jpg"%(self.image_index) ):
                                self.image_index += 1
                        else:
                                break

        def capture(self):
                
                #self.cam.capture(self.out, 'rgb', use_video_port = True)
                #p = np.array( self.out )
                #self.saver.save_data( p, self.car.get_speed(), self.car.get_normal_angle() )
                self.cam.capture("image/%08d_%d_%d.jpg"%(self.image_index, self.car.get_speed(), self.car.get_normal_angle() ),
                                 'jpeg',
                                 use_video_port = True
                                 )
                self.image_index += 1
                if self.image_index %100 == 0:
                        print("index: "+str(self.image_index))


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


class Receiver(threading.Thread):
        def __init__(self, car_object):
                threading.Thread.__init__(self)

                self.HOST=""
                self.PORT=int(input())
                self.ADDR = (self.HOST, self.PORT)

                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind( self.ADDR )
                self.sock.listen(100)
                self.status = "stop"
                self.car = car_object

        def run(self):
                global SERVER_DOWN
                self.status = "run"
                while self.status == "run":

                        conn, addr = self.sock.accept()
                        print("connection accepted")
                        while self.status == "run":


                                raw_data = conn.recv(1024)
                                data = raw_data.decode("utf8").strip()

                                if not data: break

                                print(data)
                                l = list(map(int, data.split()))

                                if len(l) > 2:
                                        continue


                                if l[0] == -1 and l[1] == -1:
                                        print("server stop")
                                        SERVER_DOWN = True
                                        conn.close()
                                        exit()

                                raw_speed = l[0]
                                raw_angle = l[1]

                                angle = 51 + ( (101 - 51) * raw_angle/100.0 )

                                # raw_angle [0,100] => angle [-45, 45] (degree) 매핑
                                # angle [-45, 45] => [-0.7853, 0.7853] (radian) 매핑

                                speed_a = (raw_angle-50)/50*45*3.141592/180


                                #if speed_a < 0:
                                #        speed_a = speed_a * 1.1
                                speed_a = speed_a * 1.2

                                speed = 1
                                if raw_speed > 0:
                                        speed = raw_speed/math.cos(speed_a)
                                else:
                                        speed = raw_speed
                                self.car.set_speed(speed)
                                self.car.set_angle(angle)

                        conn.close()

        def stop(self):
                self.status = "stop"


def main():

        car = Car()

        camera = Camera(car)
        camera.set_fps(30)
        receiver = Receiver(car)

        receiver.start()

        print("server starte")
        time.sleep(10)
        print("capture start")
        i = 0
        while True:
                try:
                        if SERVER_DOWN is True:
                                exit()
                        if i%100 and i!=0:
                                i = 0
                                print("running...")
                        else:
                                i = i+1
                        time.sleep(0.25)

                        camera.capture()

                except KeyboardInterrupt:

                        receiver.stop()
                        break


if __name__ == "__main__":
        main()
