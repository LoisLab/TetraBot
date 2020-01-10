import RPi.GPIO as GPIO
from time import sleep


class Motors:
    
    def __init__(self, motor1_pins=(8,10,12), motor2_pins=(11,13,15), motor3_pins=(33,35,37), motor4_pins=(36,38,40)):
        GPIO.setmode(GPIO.BOARD)
        self.motor1=Motor(motor1_pins)
        self.motor2=Motor(motor2_pins)
        self.motor3=Motor(motor3_pins)
        self.motor4=Motor(motor4_pins)
        
    def set_direction(self,motor1_dir,motor2_dir,motor3_dir,motor4_dir):
        self.motor1.set_direction(motor1_dir)
        self.motor2.set_direction(motor2_dir)
        self.motor3.set_direction(motor3_dir)
        self.motor4.set_direction(motor4_dir)
        
    def go(self):
        self.motor1.go()
        self.motor2.go()
        self.motor3.go()
        self.motor4.go()
        
    def stop(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()

    def cleanup(self):
        self.stop()
        GPIO.cleanup()


class Motor:
    
    FORWARD=(GPIO.HIGH,GPIO.LOW)
    REVERSE=(GPIO.LOW,GPIO.HIGH)
    OFF=(GPIO.LOW,GPIO.LOW)
    
    ACTIONS=(OFF,FORWARD,REVERSE)
    
    def __init__(self, pins):
        self.pins=pins
        GPIO.setup(self.pins[0], GPIO.OUT)
        GPIO.setup(self.pins[1], GPIO.OUT)
        GPIO.setup(self.pins[2], GPIO.OUT)
        GPIO.output(self.pins[2], GPIO.LOW)

    def set_direction(self, direction):
        GPIO.output(self.pins[0], direction[0])
        GPIO.output(self.pins[1], direction[1])
        
    def go(self):
        GPIO.output(self.pins[2], GPIO.HIGH)
        
    def stop(self):
        GPIO.output(self.pins[2], GPIO.LOW)
