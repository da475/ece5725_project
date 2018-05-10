import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)


gp.setup(21, gp.OUT)    #X1
gp.setup(20, gp.IN)    #X2
gp.setup(16, gp.OUT)    #X3


gp.output(21, gp.HIGH)
gp.output(16, gp.LOW)
time.sleep(5)


gp.cleanup()


