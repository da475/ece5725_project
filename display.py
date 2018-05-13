
import RPi.GPIO as gp
import pygame
import os
import math
import time

if 1:
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

######  GPIO  ###########
gp.setmode(gp.BCM)
gp.setup(17, gp.IN,pull_up_down=gp.PUD_UP)

signal = 0

def gp17_cb(channel):
    global signal
    signal = 1

gp.add_event_detect(17, gp.FALLING, callback=gp17_cb, bouncetime=300)

#########################

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
count = 0
size = SCREEN_WIDTH, SCREEN_HEIGHT
BLACK = (0,0,0)
BLUE = (0, 0, 255)
rect = (0, 200, SCREEN_WIDTH, 40)       # x, y, width, height

pygame.init()

screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
screen.fill(BLACK)


pygame.draw.rect(screen, BLUE, rect, 0)

while 1:

    screen.fill(BLACK)
    rect = (0, 200-count, SCREEN_WIDTH, 40+count)       # x, y, width, height
    pygame.draw.rect(screen, BLUE, rect, 0)
    pygame.display.update()
    time.sleep(0.2)
    if signal == 1:
        break

    count = count + 1
    count = count % 20


gp.cleanup()



