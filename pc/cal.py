#-*- coding:utf8 -*-

from module.networkClass import Calculator

# server에서 실행하는 python 코드
# cv2, tensorflow, numpy 모듈이 필요함

if __name__ == '__main__':
    client = Calculator('192.168.255.181',8000)
    client.start()
