
# ECE5725 Final Project Spring'18
# Date: 15th May 2018
# Authors: Anwitha Paruchuri and Deepak Agarwal
# NetIds: ap2286 and da475
# File: led_charlie_3pins.py
# Desc: Python script to implement the charlieplexing for 3-pins

import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

# set the GPIO pins as out or in
gp.setup(21, gp.OUT)    #X1
gp.setup(20, gp.OUT)    #X2
gp.setup(16, gp.IN)    #X3

# start glowing the LEDs
gp.output(21, gp.HIGH)
gp.output(20, gp.LOW)
time.sleep(5)
gp.output(21, gp.LOW)
gp.output(20, gp.HIGH)
time.sleep(5)


gp.cleanup()


