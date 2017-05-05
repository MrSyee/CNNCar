import socket
import threading
import math

class Receiver(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

                self.HOST=""
                print("input port: ")
                self.PORT=int(input())
                self.ADDR = (self.HOST, self.PORT)

                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind( self.ADDR )
                self.sock.listen(100)
                self.status = "stop"

                self.SERVER_DOWN = False
                self.car_status = {}
                self.car_status['speed'] = 0
                self.car_status['angle']=50

        def run(self):
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
                                        self.   SERVER_DOWN = True
                                        conn.close()
                                        exit()

                                raw_speed = l[0]
                                raw_angle = l[1]

                                angle = 51 + ( (101 - 51) * raw_angle/100.0 )

                                # raw_angle [0,100] => angle [-45, 45] (degree)
                                # angle [-45, 45] => [-0.7853, 0.7853] (radian)

                                speed_a = (raw_angle-50)/50*45*3.141592/180


                                #if speed_a < 0:
                                #        speed_a = speed_a * 1.1
                                speed_a = speed_a * 1.2

                                speed = 1
                                if raw_speed > 0:
                                        speed = raw_speed/math.cos(speed_a)
                                else:
                                        speed = raw_speed

                                self.car_status['speed'] = speed
                                self.car_status['angle'] = angle


                        conn.close()
        def get_speed_angle(self):
                return self.car_status


        def stop(self):
                self.status = "stop"
