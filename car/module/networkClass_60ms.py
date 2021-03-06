#-*- coding:utf8 -*-

import socket
import pickle
import time

from module.cameraClass import Camera
from module.carClass import Car
import sys
class Server:

    def __init__(self):

        # 자동차 객체 초기화 (GPiO 핀 초기화)
        self.car = Car()
        print(" [*] car object initialized")

        # 카메라 객체 초기화
        self.camera = Camera()
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


        
        while True:
            print(" [*] connection waiting")
            self.connection, self.client_address = self.sock.accept()
            print(" [*] connection accepted. {}".format(self.client_address))       

            # 폴더에 저장된 image를 순차적으로 전송함
            try:
                while True:

                    # ----------------------------------------
                    # send -----------------------------------
                    # ----------------------------------------

                    c = time.time()
                    stream = self.camera.capture()
                    ct = time.time()
                    self.connection.send( stream  )
                    self.connection.send( b'end' )
                    c1 = time.time()

                    # ----------------------------------------
                    # recv -----------------------------------
                    # ----------------------------------------

                    d = self.connection.recv(256)
                    print(len(d))
                    c2 = time.time()
                    try:
                        # byte로 이루어진 dict 데이터를 복원함
                        data = pickle.loads( d )
                    except:
                        # 복원에 실패할 경우 기본 데이터를 사용한다
                        print("except occur!!!")
                        data = {'speed':35, 'angle':50}
                    #sys.stdout.write('\r')
                    #sys.stdout.write(" [*] %.5f %.5f  " % (data['speed'], data['angle']))
                    #sys.stdout.flush()

                    self.car.set_speed_angle( data['speed'], data['angle'] )
                    #print("%.5f %.5f" %(data['speed'],data['angle']) )
                    print("time : %.5f %.5f %.5f %.5f" % ( ct-c, c1-ct, c2-c1, time.time()-c2 ) )
            
            except:
                pass

            finally:
                self.connection.close()
                print("\n [*] connection closed")
                #self.sock.close()
