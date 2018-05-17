
# ECE5725 Final Project Spring'18
# Date: 15th May 2018
# Authors: Anwitha Paruchuri and Deepak Agarwal
# NetIds: ap2286 and da475
# File: display.py
# Desc: Python script to implement the flood wall on display monitor
#       Note: This is just a helper file

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
size = SCREEN_WIDTH, SCREEN_HEIGHT
BLACK = (0,0,0)
YELLOW = (225,225,0)
PINK = (255,105,180)
BLUE = (0, 0, 255)
rect = (0, 200, SCREEN_WIDTH, 40)       # x, y, width, height

pygame.init()

screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(True)
screen.fill(YELLOW)


# water level display

#xpos_level = int((45/320) * SCREEN_WIDTH)
xpos_level = 80
level_list = {  '0"-1.5": NO FLOOD':(xpos_level,20), 
                '1.5"-2.0": MODERATE FLOOD STAGE-1':(xpos_level, 30),
                '2.0"-2.5": MODERATE FLOOD STAGE-2':(xpos_level, 40),
                '2.5"-3.0": FLOOD STAGE-1':(xpos_level, 50),
                '3.0"-3.5": FLOOD STAGE-2':(xpos_level, 60),
                '3.5"-4.0": CRITICAL FLOOD STAGE-1':(xpos_level, 70),
                '4.0"-4.5": CRITICAL FLOOD STAGE-2':(xpos_level, 80),
            }

pygame.draw.rect(screen, BLUE, rect, 0)
menu_font = pygame.font.Font(None, 10)


# setting for current range
current_msg_pos = (220, 30)
current_msg_font = pygame.font.Font(None, 25)
current_number_pos = (220, 60)
current_number_font = pygame.font.Font(None, 25)

# FISH
FISH_WIDTH = 300
FISH_HEIGHT = 20
fish_pos = (30, 180)
speed =[1,1]

fish = pygame.image.load("fish.png")
fish = pygame.transform.scale(fish, (70,70))
br1 = fish.get_rect(center = fish_pos)
br1.left = 30


count = 0
offset = 937

while(1):

  # display fish
  br1 = br1.move(speed)
  if br1.left < 0 or br1.right > FISH_WIDTH:
      speed[0] = -speed[0]
  
  if br1.top < 0 or br1.bottom > FISH_HEIGHT:
      speed[1] = -speed[1]

  screen.blit(fish , br1)
 

  # display level
  rect = (0, 200-count, SCREEN_WIDTH, 40+count)       # x, y, width, height
  pygame.draw.rect(screen, BLUE, rect, 0)
  pygame.display.update()


  # display the menu
  for menu_text, menu_pos in level_list.items():
      text_surface = menu_font.render(menu_text, True, BLUE)
      rect = text_surface.get_rect(center=menu_pos)
      screen.blit(text_surface, rect)


  # display the current range in txt
  text_surface = current_msg_font.render('FLOOD LEVEL', True, BLUE)
  rect = text_surface.get_rect(center=current_msg_pos)
  screen.blit(text_surface, rect)


  # display the current number 
  level = offset + (count * 100)
  level = float(level / 500.0)
  number_str = str(level)
  text_surface = current_number_font.render(number_str, True, BLUE)
  rect = text_surface.get_rect(center=current_number_pos)
  screen.blit(text_surface, rect)


  pygame.display.flip()

  time.sleep(0.2)
  screen.fill(YELLOW)


  count = count + 1
  count = count % 20

  if signal == 1:
      break


gp.cleanup()



