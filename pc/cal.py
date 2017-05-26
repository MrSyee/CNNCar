#-*- coding:utf8 -*-

import sys
from module.networkClass import Calculator

# server에서 실행하는 python 코드
# cv2, tensorflow, numpy 모듈이 필요함

if __name__ == '__main__':


    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    client = Calculator('192.168.255.181',port)
    client.start()

    cv2.destroyAllWindows()
