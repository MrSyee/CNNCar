# -*- coding:utf8 -*-
import socket
import pickle
import cv2
import numpy as np
import sys
import select

import time


class Network:
    def __init__(self, address, port):

        # 연결 소켓 초기화
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server = (address, port)
            self.sock.connect(server)
            self.sock.setblocking(0)

        except BaseException as e:
            print(" [E] {}".format(e.args))
            print(" [*] calculator initializing failed")
            exit()

        print(" [*] calculator ready")

        # 멤버변수 선언
        self.count = 0  # 처리한 스트림 갯수 저장
        self.remain = b''

    def recv(self):
        t = time.time()

        stream_bytes = b'' + self.remain

        if len(self.remain) > 0:
            self.remain = 0
        start_byte = b'\xff\xd8'
        end_byte = b'\xff\xd9'
        while True:
            if time.time() - t > 0.5:
                print("\nTIMEOUT")
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

                stream_bytes = stream_bytes[:end_point + 2]
                self.remain = stream_bytes[end_point + 3:]
                break
        sys.stdout.write('\r')
        sys.stdout.write(" [*] recv end. length: %6d, count: %6d" % (len(stream_bytes), self.count))
        sys.stdout.flush()
        self.count += 1

        return stream_bytes

    def send(self, byte):
        self.sock.send(byte)

    def __del__(self):
        self.sock.close()
