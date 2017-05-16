#-*- coding:utf8 -*-

from module.networkClass import Server

# 테스트를 위해 window에서도 돌아가게 만든 유사 client
# raspberry pi에서 쓰는 GPiO, PiCamera 모듈을 쓰지 않음
# 폴더에서 image를 읽어와 byte화하여 server로 전송하고 결과값을 받아옴

if __name__ == '__main__':

    server = Server()
    server.start()
