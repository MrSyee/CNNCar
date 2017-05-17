#-*- coding:utf8 -*-

import socket
import pickle
import time
import io
import picamera

from module.carClass import Car
import sys
class Server:

    def __init__(self):

        # 자동차 객체 초기화 (GPiO 핀 초기화)
        self.car = Car()
        print(" [*] car object initialized")

        # 카메라 객체 초기화
        print(" [*] camera object initialized")

        # 소켓 연결 초기화
        self.port = 8000
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server = ('', self.port)
            self.sock.bind(self.server)
            self.sock.listen(1)
        except BaseException as e:
            print(" [*] server initializing failed")
            print(" [E] {}".format(e.args) )
            exit()

        print(" [*] car ready")
        print(" [*] IP: {} PORT: {}".format(self.what_is_my_ip(),self.port))


    def what_is_my_ip(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('www.google.com',0))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    def start(self):

        camera = picamera.PiCamera()
        camera.resolution = (128,96)
        camera.framerate = 30
        camera.rotation = 180
        #camera.ISO = 300

        
        while True:
            print(" [*] connection waiting")
            self.connection, self.client_address = self.sock.accept()
            print(" [*] connection accepted. {}".format(self.client_address))
            
            time.sleep(1) 
            stream = io.BytesIO()
            
            # 폴더에 저장된 image를 순차적으로 전송함
            try:
                #while True:
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    
                    # ----------------------------------------
                    # send -----------------------------------
                    # ----------------------------------------

                    
                    self.connection.send( stream.getvalue()  )
                    stream.seek(0)

                    # ----------------------------------------
                    # recv -----------------------------------
                    # ----------------------------------------

                    d = self.connection.recv(256)
                    try:
                        # byte로 이루어진 dict 데이터를 복원함
                        data = pickle.loads( d )
                    except:
                        # 복원에 실패할 경우 기본 데이터를 사용한다
                        print("except occur!!!")
                        data = {'speed':35, 'angle':50}

                    self.car.set_speed_angle( data['speed'], data['angle'] )
                    

                    
            except BaseException as e:
                print("{}".format(e.args))
                pass

            finally:
                self.connection.close()
                self.car.set_speed_angle(0,50)
                print("\n [*] connection closed")
                #self.sock.close()
