import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

#pin_ledR = 5
#pin_ledG = 22

#gp.setup(pin_led1, gp.OUT)
#gp.setup(pin_led1, gp.OUT)
#gp.setup(pin_led3, gp.IN)

#gp.setup(17, gp.OUT)
#gp.setup(5, gp.OUT)
gp.setup(4, gp.OUT)
#gp.setup(23, gp.IN)

#gp.output(17, gp.HIGH)
gp.output(4, gp.HIGH)
#gp.output(4, gp.LOW)
#gp.output(25, gp.HIGH)

time.sleep(5)

"""
p_red = gp.PWM(pin_ledR, 1)     # 1Hz freq
p_green = gp.PWM(pin_ledG, 1)     # 1Hz freq

p_red.start(50)                 # start with 50% duty cycle
p_green.start(50)                 # start with 50% duty cycle
time.sleep(3)

p_red.ChangeFrequency(2)
p_green.ChangeFrequency(0.6)
time.sleep(3)

p_red.ChangeFrequency(4)
p_green.ChangeFrequency(0.3)
time.sleep(3)

p_red.stop()
p_green.stop()
"""

gp.cleanup()


