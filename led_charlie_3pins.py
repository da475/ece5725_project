import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)


gp.setup(21, gp.OUT)    #X1
gp.setup(20, gp.OUT)    #X2
gp.setup(16, gp.IN)    #X3


gp.output(21, gp.HIGH)
gp.output(20, gp.LOW)
time.sleep(5)
gp.output(21, gp.LOW)
gp.output(20, gp.HIGH)
time.sleep(5)


gp.cleanup()


