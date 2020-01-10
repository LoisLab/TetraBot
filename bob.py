from motor_lib import *
import random
import copy


class Bob:
    
    def __init__(self, speed=1):
        self.motors = Motors()
        self.speed = speed

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
        sleep(1)
        self.motors.stop()
        
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
        html = 'A robot with four motors and three actions per motor (off, forward, reverse) will have 3^4 possible actions;<br>'
        html += 'provide a command via the URL above in the format http://loislabpi-14.local/action=xx where xx is a number from 0 to 80<br>'
        return html
    

    