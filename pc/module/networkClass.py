#-*- coding:utf8 -*-
import socket
import pickle
import cv2
import numpy as np
import sys
import select

import time
from module.tensorClass import Tensor
import module.redParser as Red


class Calculator:
    def __init__(self,address,port):
        # 텐서플로우 초기화
        self.session = Tensor()


        # 연결 소켓 초기화
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server = (address, port)
            self.sock.connect(server)
            self.sock.setblocking(0)

        except BaseException as e:
            print(" [E] {}".format(e.args) )
            print(" [*] calculator initializing failed")
            exit()

        print(" [*] calculator ready")

        
        # 멤버변수 선언
        self.data = { 'speed':30, 'angle':50 }
        self.total_time = 0  # 총 연산 시간 저장
        self.count = 0       # 처리한 스트림 갯수 저장


        self.remain = b''
        self.move = [50]*10
    def get_move(self,new):
        self.move = self.move[1:]
        self.move.append(new)
        return np.average(self.move + [new]*10)

    def recv(self):
        t = time.time()
        stream_bytes = b'' + self.remain

        if len(self.remain) > 0:
            self.remain = 0
        start_byte = b'\xff\xd8'
        end_byte = b'\xff\xd9'
        while True:
            if time.time() - t > 0.5:
                print("TIMEOUT")
                return -1
            # 한 이미지가 차지하는 byte의 양은 4096개보다 많으므로
            # 여러번 루프를 돌면서 jpeg의 마지막인 b'\xff\xd9'를 만날 때까지 stream을 저장함
            ready = select.select([self.sock], [], [], 0.2)
            if ready[0]:
                stream_bytes += self.sock.recv(4096)
            
            start_point = stream_bytes.find(start_byte)
            end_point = stream_bytes.find(end_byte)
                
            if end_point > 0:
                if start_point == -1:
                    stream_bytes = b''
                    continue
                
                stream_bytes = stream_bytes[:end_point+2]
                self.remain = stream_bytes[end_point+3:]
                break
        sys.stdout.write('\r')
        sys.stdout.write(" [*] recv end. length: %4d, count: %4d" % (len(stream_bytes), self.count))
        sys.stdout.flush()
        self.count += 1
        
        return stream_bytes
            
                
        

    def start(self):

        former_angle = 50

        try:
            while True:
                # byte로 저장된 image를 server로부터 받아 저장함
                t = time.time()
                raw = self.recv()
                if raw == -1:
                    self.sock.send( pickle.dumps(self.data) )
                    continue

                # byte image를 numpy array로 변환
                img = cv2.imdecode( np.fromstring(raw, dtype=np.uint8), cv2.IMREAD_COLOR )

                # numpy array로 제대로 변환되었는지 확인
                if 'T' in dir(img):
                    
                    angle = self.session.run(img) * 100
                    cv2.imshow("img",img)
                    cv2.waitKey(1)
                else:
                    angle = 50


                self.data['angle'] = angle
                self.data['speed'] = 65


                
                #if Red.get_red_pixel_num(img) > 5:    
                #    self.data['speed'] = 0
                #else:
                #    self.data['speed'] = 25
                
                # pickle를 이용해 dict 배열을 byte로 변환한 후 소켓으로 전송함
                self.sock.send( pickle.dumps(self.data) )
                         
                self.total_time += (time.time() - t)
                
        except KeyboardInterrupt:
            print(" [*] calculator stop")

        #except BaseException as error:
        #    print("\n [E] {}".format(error.args))

        finally:
            print(" [*] Average processing time: %f" % (float(self.total_time)/self.count))
            self.sock.close()

