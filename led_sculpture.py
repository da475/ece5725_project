import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

#pin_ledR = 5
#pin_ledG = 22

#gp.setup(pin_led1, gp.OUT)
#gp.setup(pin_led1, gp.OUT)
#gp.setup(pin_led3, gp.IN)

#gp.setup(17, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(4, gp.OUT)
#gp.setup(23, gp.IN)

#gp.output(17, gp.HIGH)
gp.output(4, gp.HIGH)
gp.output(21, gp.HIGH)
#gp.output(25, gp.HIGH)

time.sleep(20)


gp.cleanup()


