import time
from motor_lib import *
import random
import copy
import busio
from mpu6050 import mpu6050


class Bob:
    
    def __init__(self, speed=1):
        self.motors = Motors()
        self.speed = speed
        self.calibrate_gyro = (-4.8,1.35,-1.15)
        self.mpu = mpu6050(0x68)
        self.rotation = {}
        self.orientation = {}

    def gyro_nap(self, seconds=1):
        xrot, yrot, zrot = 0,0,0
        t0 = time.time()
        t_stop = t0 + seconds
        while t0 < t_stop:
            gyro_data = self.mpu.get_gyro_data()
            t1=time.time()
            dt = t1 - t0
            xrot += (gyro_data['x'] - self.calibrate_gyro[0]) * dt
            yrot += (gyro_data['y'] - self.calibrate_gyro[1]) * dt
            zrot += (gyro_data['z'] - self.calibrate_gyro[2]) * dt
            t0 = t1
        self.rotation = {'xr':xrot,'yr':yrot,'zr':zrot}

    def make_base3(self, action_number):
        action = []
        for i in range (3,-1,-1):
            ans, action_number=divmod(action_number,3**i)
            action.append(ans)
        return action
        
    def sample(self):
        action_number = random.randint(0,80)
        return self.make_base3(action_number)
        
    def step(self, action):
        self.motors.set_direction(Motor.ACTIONS[action[0]],Motor.ACTIONS[action[1]],Motor.ACTIONS[action[2]],Motor.ACTIONS[action[3]])
        self.motors.go()
        self.gyro_nap(1)
        self.motors.stop()
        print(self.rotation)
        time.sleep(.25)
        self.orientation = self.mpu.get_accel_data()
        print(self.orientation)
        
    def listen(self, message):
        tokens = message.split('=')
        if len(tokens)==2 and tokens[0]=='action':
            self.step(self.make_base3(int(tokens[1])))
        elif len(tokens)==2 and tokens[0]=='speed':
            self.speed = float(tokens[1])
        else:
            raise ValueError('Unknown command: ' + message)
   
    def shutdown(self):
        self.motors.stop()
        GPIO.cleanup()
        
    def get_homepage(self):
        html=''
        #html = 'A robot with four motors and three actions per motor (off, forward, reverse) will have 3^4 possible actions;<br>'
        #html += 'provide a command via the URL above in the format http://loislabpi-14.local/action=xx where xx is a number from 0 to 80<br>'
        return html
    

    