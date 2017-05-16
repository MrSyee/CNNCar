#-*- coding:utf8 -*-
import socket
import pickle
import cv2
import numpy as np
import sys

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

        except:
            print(" [*] calculator initializing failed")
            exit()

        print(" [*] calculator ready")


        # 멤버변수 선언
        self.data = { 'speed':30, 'angle':50 }
        self.total_time = 0  # 총 연산 시간 저장
        self.count = 0       # 처리한 스트림 갯수 저장




    def recv(self):
        stream_bytes = b''

        while True:

            # 한 이미지가 차지하는 byte의 양은 2048개보다 많으므로
            # 여러번 루프를 돌면서 b'end'를 만날 때까지 stream을 저장함
            stream_bytes += self.sock.recv(4096)
            if b'end' in stream_bytes:
                endpoint = stream_bytes.find(b'end')
                stream_bytes = stream_bytes[:endpoint]

                break
        sys.stdout.write('\r')
        sys.stdout.write(" [*] recv end. length: %4d, count: %4d" % (len(stream_bytes), self.count))
        sys.stdout.flush()
        self.count += 1

        return stream_bytes




    def start(self):

        try:
            while True:

                # byte로 저장된 image를 server로부터 받아 저장함
                raw = self.recv()
                t = time.time()

                #print(str(raw.find('\xff\xd8'))+" "+str(raw.find('\xff\xd9')+2))

                # byte image를 numpy array로 변환
                img = cv2.imdecode( np.fromstring(raw, dtype=np.uint8), cv2.IMREAD_COLOR )

                # numpy array로 제대로 변환되었는지 확인
                if 'T' in dir(img):
                    angle = self.session.run(img) * 100
                else:
                    angle = 50

                #cv2.imshow("image",img)
                #cv2.waitKey(1)

                self.data['angle'] = angle
                if Red.get_red_pixel_num(img) > 10:

                    self.data['speed'] = 0
                else:
                    self.data['speed'] = 35

                # pickle를 이용해 dict 배열을 byte로 변환한 후 소켓으로 전송함
                self.sock.send( pickle.dumps(self.data) )
                self.total_time += (time.time() - t)

        except KeyboardInterrupt:
            print(" [*] calculato stop")

        except BaseException as error:
            print("\n [E] {}".format(error.args))

        finally:
            print(" [*] Average processing time: %f" % (float(self.total_time)/self.count))
            self.sock.close()
