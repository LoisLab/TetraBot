from motor_lib import *
import random
import copy

class ActionSpace:
    
    ACTIONS = [(Motor.FORWARD, Motor.REVERSE, 0.15),
               (Motor.FORWARD, Motor.REVERSE, 0.30),
               (Motor.REVERSE, Motor.FORWARD, 0.15),
               (Motor.REVERSE, Motor.FORWARD, 0.30),
               (Motor.FORWARD, Motor.FORWARD, 0.25),
               (Motor.FORWARD, Motor.FORWARD, 0.50),
               (Motor.REVERSE, Motor.REVERSE, 0.25),
               (Motor.REVERSE, Motor.REVERSE, 0.50)]
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.actions = copy.deepcopy(ActionSpace.ACTIONS)
             
    def actions(self):
        return self.actions
    
    def sample(self):
        return self.actions[random.randint(1,len(self.actions))]
    
    def reorder(self):
        reordered = []
        while len(self.actions)>0:
            reordered.append(self.actions.pop(random.randint(0,len(self.actions)-1)))
        self.actions = reordered
        
    def randomize(self):
        self.actions = []
        for n in range(random.randint(4,12)):
            left = Motor.REVERSE if random.random()<.5 else Motor.FORWARD
            right = Motor.REVERSE if random.random()<.5 else Motor.FORWARD
            duration = 0.10+random.random()/2
            self.actions.append((left,right,duration))

class Bob:
    
    def __init__(self, speed=1):
        self.action_space = ActionSpace()
        self.motors = Motors()
        self.speed = speed
        
    def step(self, action):
        self.motors.set_direction(action[0],action[1])
        self.motors.go()
        sleep(action[2]*self.speed)
        self.motors.stop()
        
    def listen(self, message):
        tokens = message.split('=')
        if len(tokens)==2 and tokens[0]=='action':
            self.step(self.action_space.actions[int(tokens[1])])
        elif len(tokens)==2 and tokens[0]=='speed':
            self.speed = float(tokens[1])
        elif len(tokens)==2 and tokens[0]=='config':
            if tokens[1]=='reorder':
                self.action_space.reorder()
            elif tokens[1]=='randomize':
                self.action_space.randomize()
            elif tokens[1]=='reset':
                self.action_space.reset()
            else:
                raise ValueError('Unknown configuration: ' + message)
        else:
            raise ValueError('Unknown command: ' + message)
   
    def shutdown(self):
        self.motors.stop()
        GPIO.cleanup()
        
    def get_homepage(self):
        html = '<b>action space</b><br>'
        for x in range(len(self.action_space.actions)):
            html += '<a href=http://%ip%/action='+str(x)+'>action '+str(x)+'</a><br>'
        html += '<br><a href=http://%ip%/config=reorder>reorder</a>'
        html += '<br><a href=http://%ip%/config=randomize>randomize</a>'
        html += '<br><a href=http://%ip%/config=reset>reset</a>'
        return html
        
        
    