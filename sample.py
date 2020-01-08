from time import sleep
from motor_lib import *

m = Motors()

for i in range(10):
    m.set_direction(Motor.OFF,Motor.OFF,Motor.FORWARD,Motor.FORWARD)
    m.go()
    sleep(1)
    m.stop()
    
    m.set_direction(Motor.OFF,Motor.REVERSE,Motor.REVERSE,Motor.OFF)
    m.go()
    sleep(1)
    m.stop()

'''m.set_direction(Motor.FORWARD,Motor.REVERSE,Motor.FORWARD,Motor.REVERSE)
m.go()
sleep(1)
m.stop()

m.set_direction(Motor.REVERSE,Motor.FORWARD,Motor.REVERSE,Motor.FORWARD)
m.go()
sleep(1)
m.stop()
'''

m.cleanup()