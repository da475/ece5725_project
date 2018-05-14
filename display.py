
import RPi.GPIO as gp
import pygame
import os
import math
import time

from pygame.locals import*

######  GPIO  ###########

piTFT = 0

if piTFT:
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


pygame.init()

if piTFT:
    pygame.mouse.set_visible(False)
else:
    pygame.mouse.set_visible(True)

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
YELLOW = (255,255,0)
PINK = (255,105,180)
BLUE = (0, 0, 255)
rect = (0, 200, SCREEN_WIDTH, 40)       # x, y, width, height

pygame.init()

screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(True)
screen.fill(YELLOW)


# water level display
pygame.draw.rect(screen, PINK, rect, 0)
my_font = pygame.font.Font(None, 30)
my_text = 'WATER LEVEL'
text_pos = (200, 30)


# FISH
FISH_WIDTH = 300
FISH_HEIGHT = 20
speed =[1,1]

fish = pygame.image.load("fish.png")
fish = pygame.transform.scale(fish, (70,70))
br1 = fish.get_rect()

radius = 64
dia = 128*128


while 1:
    br1 = br1.move(speed)

    if br1.left < 0 or br1.right > FISH_WIDTH:
        speed[0] = -speed[0]
    
    if br1.top < 0 or br1.bottom > FISH_HEIGHT:
        speed[1] = -speed[1]

    screen.blit(fish , br1)
   

    rect = (0, 200-count, SCREEN_WIDTH, 40+count)       # x, y, width, height
    pygame.draw.rect(screen, PINK, rect, 0)
    pygame.display.update()

    count = count + 1
    count = count % 20


    text_surface = my_font.render(my_text, True, BLUE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)


    pygame.display.flip()

    time.sleep(0.2)
    screen.fill(YELLOW)


    if signal == 1:
        break


gp.cleanup()



