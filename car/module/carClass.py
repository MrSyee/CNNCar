import RPi.GPIO as GPIO
import math
GPIO.setwarnings(False)



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

        def set_speed_angle(self, raw_speed, raw_angle):
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
                self.set_speed(speed)
                self.set_angle(angle)

                print("%2.5f %2.5f" % (speed,raw_angle) )
