

# ECE5725 Final Project Spring'18
# Date: 15th May 2018
# Authors: Anwitha Paruchuri and Deepak Agarwal
# NetIds: ap2286 and da475
# File: ultrasonic_bt_charlie.py
# Desc: Python script to implement the client side in RPi-0
#       It does the following:
#       - Sets up the bluetooth connection with the server
#       - Configures the ultrasonic sensor and sets the callback method
#       - Receives sensor values and sends it over the bluetooth
#       - Creates object of the class charlie() to configure the LEDs

import bluetooth
import RPi.GPIO as gp
import time
from led_charlie import *

gp.setmode(gp.BCM)

# macros
MIN_DIST = 1000
MAX_DIST = 3500
MID_DIST = int((MIN_DIST + MAX_DIST) / 2)
OFFSET = int( (MAX_DIST - MIN_DIST) / 6 )

# pin definitions
pin_ledR = 4
pin_ledG = 5
pin_quit = 18
gp_trigger = 13
gp_echo = 26

# vars initialization
start_time = 0
duration = 0
quit_signal = 0
RECV_SIZE = 1024
server_port = 71

gp.setup(pin_quit, gp.IN, pull_up_down=gp.PUD_UP)
gp.setup(pin_ledR, gp.OUT)
gp.setup(pin_ledG, gp.OUT)
gp.setup(gp_trigger, gp.OUT)
gp.setup(gp_echo, gp.IN)

# setup PWM for the leds
p_red = gp.PWM(pin_ledR, 1)     # 1Hz freq
p_green = gp.PWM(pin_ledG, 1)     # 1Hz freq

# start with initial duty cycle for green and red LEDs
p_red.start(0)                  # start with 0% duty cycle
p_green.start(50)               # start with 100% duty cycle


###### CLIENT - RPi0 ###########

# create a client socket and connect to the server
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect(("B8:27:EB:7E:2A:D0", 3))
client_socket.send("Very Horrible Ani")
print "Horrible Ani finished"


# quit button
def gp18_cb(channel):
    global quit_signal
    quit_signal = 1

gp.add_event_detect(pin_quit, gp.FALLING, callback=gp18_cb, bouncetime=300)

############### SENSOR ########################
# Sensor callback
def gp26_cb(channel):
    global start_time
    global duration

    value = gp.input(gp_echo)
    #print("input changed to = ", value)

    if value == gp.HIGH:
        start_time = time.time()
    else:
        end_time = time.time()
        duration = (end_time - start_time) * 1000000
        duration = int(duration)
        print ('dur in us is ', duration)

gp.add_event_detect(gp_echo, gp.BOTH, callback=gp26_cb, bouncetime=1)


############### SENSOR ########################

def start_sensing():
    gp.output(gp_trigger, gp.LOW)
    charlie_obj = charlie()
    #charlie_obj.glow_led1()
    #charlie_obj.glow_led2()

    while(1):
        # send the trigger pulse
        gp.output(gp_trigger, gp.HIGH)
        time.sleep(20/1000000.0)
        gp.output(gp_trigger, gp.LOW)

        # wait for 100ms
        time.sleep(0.1)


        # level 1 (when water level is too high)
        if duration < MIN_DIST + OFFSET:
            charlie_obj.glow_led8()
            charlie_obj.glow_led11()

        # level 2
        elif duration < MIN_DIST + (OFFSET*2):
            charlie_obj.glow_led12()
            charlie_obj.glow_led9()

        # level 3
        elif duration < MIN_DIST + (OFFSET*3):
            charlie_obj.glow_led10()
            charlie_obj.glow_led7()

        # level 4
        elif duration < MIN_DIST + (OFFSET*4):
            charlie_obj.glow_led6()
            charlie_obj.glow_led5()

        # level 5
        elif duration < MIN_DIST + (OFFSET*5):
            charlie_obj.glow_led4()
            charlie_obj.glow_led1()

        # level 6
        elif duration < MIN_DIST + (OFFSET*5):
            charlie_obj.glow_led2()
            charlie_obj.glow_led3()

        #default case
        #else:
            #print ('Out of range')

        # send the data to the server
        client_socket.send(str(duration))
        #msg_buffer = client_socket.recv(RECV_SIZE)
        #print ('C: received from server ', msg_buffer)

        if quit_signal == 1:
            print 'Quit pressed, breaking out of the loop'
            break

    # cleanup code
    # close the sockets
    time.sleep(0.2)
    client_socket.close()

    # stop pwms (todo remove it later)
    p_red.stop()
    p_green.stop()
    gp.cleanup()


start_sensing()




########################### END OF FILE ##############################






# ECE5725 Final Project Spring'18
# Date: 15th May 2018
# Authors: Anwitha Paruchuri and Deepak Agarwal
# NetIds: ap2286 and da475
# File: server.py
# Desc: Python script to implement the base station in RPI-3
#       It does the following:
#       - Sets up the bluetooth connection
#       - Receives sensor values from the client and process them
#       - Implements the flood wall via pygames library

import bluetooth
import RPi.GPIO as gp
import pygame
import os
import math
import time


# Display settings

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



############ PYGAME #############


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

# FISH settings
FISH_WIDTH = 300
FISH_HEIGHT = 20
fish_pos = (30, 180)
speed =[1,1]

fish = pygame.image.load("fish.png")
fish = pygame.transform.scale(fish, (70,70))
br1 = fish.get_rect(center = fish_pos)
br1.left = 30


################  SENSOR CAPPING #################


MIN_LEVEL = 980
MAX_LEVEL = 3500
prev_water_level = 1800


############ BLUETOOTH #############


pin_bt = 13
gp.setmode(gp.BCM)
gp.setup(pin_bt, gp.OUT)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

RECV_SIZE = 1024

# setup port number and address
server_port = 3
server_addr = ""

# restart the server
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# create welcoming socket and listen to 1 client
server_socket.bind((server_addr, server_port))
server_socket.listen(1)

# look for the client connection
client_socket, client_address = server_socket.accept()
print ('recevied connection from ', client_address)
msg_buffer = client_socket.recv(RECV_SIZE)
print(msg_buffer)


# start loop to receive msgs until client closes
while True:
    msg_buffer = client_socket.recv(RECV_SIZE)
    if not msg_buffer:
        print 'Client closed, breaking out of the loop'
        break


    # send the data back to the client
    print ('\nrecvd the msg ', msg_buffer)
    water_level = int(msg_buffer)
    #msg = str(water_level)
    #client_socket.send(msg)

    # calculate the water level
    #water_level = water_level - MIN_LEVEL
    #water_level = int(water_level / 50)


    # cap it

    if water_level < MIN_LEVEL:
        water_level = prev_water_level
    elif water_level > MAX_LEVEL:
        water_level = prev_water_level
    else:
        prev_water_level = water_level 

    # MAX level is actually the MIN because when distance
    # is maximum, the level is minimum
    water_level = MAX_LEVEL + MIN_LEVEL - water_level
 

    ################  NEW CODE  #####################


    # display level
    display_level = int(water_level / 50)
    rect = (0, 200-display_level, SCREEN_WIDTH, 40+display_level)       # x, y, width, height
    pygame.draw.rect(screen, BLUE, rect, 0)
    pygame.display.update()


    # display the menu
    for menu_text, menu_pos in level_list.items():
        text_surface = menu_font.render(menu_text, True, BLUE)
        rect = text_surface.get_rect(center = menu_pos)
        screen.blit(text_surface, rect)


    # display the current range in txt
    text_surface = current_msg_font.render('FLOOD LEVEL (in inches)', True, BLUE)
    rect = text_surface.get_rect(center=current_msg_pos)
    screen.blit(text_surface, rect)


    # display the current number 
    level = float(water_level / 700.0)
    number_str = str(level)
    text_surface = current_number_font.render(number_str, True, BLUE)
    rect = text_surface.get_rect(center = current_number_pos)
    screen.blit(text_surface, rect)

    # display fish
    br1 = br1.move(speed)
    if br1.left < 0 or br1.right > FISH_WIDTH:
        speed[0] = -speed[0]
    
    if br1.top < 0 or br1.bottom > FISH_HEIGHT:
        speed[1] = -speed[1]

    screen.blit(fish , br1)
    pygame.display.flip()
    time.sleep(0.2)
    screen.fill(YELLOW)

    if signal == 1:
        break

    ## ENF OF WHILE


# close the sockets
client_socket.close()
server_socket.close()
gp.cleanup()





########################### END OF FILE ##############################





# ECE5725 Final Project Spring'18
# Date: 15th May 2018
# Authors: Anwitha Paruchuri and Deepak Agarwal
# NetIds: ap2286 and da475
# File: led_charlie.py
# Desc: Python script to implement the charlieplexing for 4-pins
#       It was implemented in a class charlie() whose object is
#       instantiated in the client code to configure the LEDs.
#       Adopting the OOPS methodology helped a lot in code-reuse.

import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

led_x1 = 21
led_x2 = 20
led_x3 = 16
led_x4 = 23
delay = 1

class charlie():
    def __init__(self):
        print ('in construct')

        gp.setup(led_x1, gp.IN)    #X1
        gp.setup(led_x2, gp.IN)     #X2
        gp.setup(led_x3, gp.OUT)    #X3
        gp.setup(led_x4, gp.OUT)    #X4

    def glow_led(self, x1, x2, x3, x4):
        gp.setup(x1, gp.OUT)    # high
        gp.setup(x2, gp.OUT)     # low
        gp.setup(x3, gp.IN)    #high-impedance
        gp.setup(x4, gp.IN)    #high-impedance
        gp.output(x1, gp.HIGH)
        gp.output(x2, gp.LOW)
        
    def glow_led1(self):
        self.glow_led(led_x1, led_x2, led_x3, led_x4)    # led1
        print ('led1')
        time.sleep(delay)

    def glow_led2(self):
        self.glow_led(led_x2, led_x1, led_x3, led_x4)    # led4
        print ('led2')
        time.sleep(delay)

    def glow_led3(self):
        self.glow_led(led_x2, led_x3, led_x1, led_x4)    # led2
        print ('led3')
        time.sleep(delay)

    def glow_led4(self):
        self.glow_led(led_x3, led_x2, led_x1, led_x4)    # led5
        print ('led4')
        time.sleep(delay)

    def glow_led5(self):
        self.glow_led(led_x1, led_x3, led_x2, led_x4)    # led7
        print ('led5')
        time.sleep(delay)

    def glow_led6(self):
        self.glow_led(led_x3, led_x1, led_x2, led_x4)    # led8
        print ('led6')
        time.sleep(delay)



    def glow_led7(self):
        self.glow_led(led_x3, led_x4, led_x1, led_x2)    # led3
        print ('led7')
        time.sleep(delay)

    def glow_led8(self):
        self.glow_led(led_x4, led_x3, led_x1, led_x2)    # led6
        print ('led8')
        time.sleep(delay)

    def glow_led9(self):
        self.glow_led(led_x2, led_x4, led_x1, led_x3)    # led9
        print ('led9')
        time.sleep(delay)

    def glow_led10(self):
        self.glow_led(led_x4, led_x2, led_x1, led_x3)    # led10
        print ('led10')
        time.sleep(delay)

    def glow_led11(self):
        self.glow_led(led_x1, led_x4, led_x2, led_x3)    # led11
        print ('led11')
        time.sleep(delay)

    def glow_led12(self):
        self.glow_led(led_x4, led_x1, led_x2, led_x3)    # led12
        print ('led12')
        time.sleep(delay)



co = charlie()

if 0:
    co.glow_led1()
    co.glow_led2()
    co.glow_led3()
    co.glow_led4()
    co.glow_led5()
    co.glow_led6()
    co.glow_led7()
    co.glow_led8()
    co.glow_led9()
    co.glow_led10()
    co.glow_led11()
    co.glow_led12()




gp.cleanup()












# ECE5725 Final Project Spring'18
# Date: 15th May 2018
# Authors: Anwitha Paruchuri and Deepak Agarwal
# NetIds: ap2286 and da475
# File: client.py
# Desc: Python script to implement the client side of the bluetooth module
#       Note: This is just a helper file, not the main file



import bluetooth
import RPi.GPIO as gp
import time

###### CLIENT - RPi0 ###########

RECV_SIZE = 1024

ack_recvd = 0

# setup port number and address
server_port = 71

# restart the server
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# create a client socket and connect to the server
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect(("B8:27:EB:7E:2A:D0", 3))
client_socket.send("Very Horrible Ani")
print "Horrible Ani finished"

count = 0
# start loop to receive msgs from server
while True:
    #msg_buffer = client_socket.recv(RECV_SIZE)
    #print ('C: recvd msg: {}'.format(msg_buffer))
    #if msg_buffer == '':
        #break

    #if ack_recvd == 0 and msg_buffer == 'ACK':
        #print ('ACK received fromt the server')
        #ack_recvd = 1
    #else:
    client_socket.send(str(count))
    msg_buffer = client_socket.recv(RECV_SIZE)
    print ('C: received from server ', msg_buffer)
    count = count+1
    if count == 5:
        break
        

# close the sockets
time.sleep(0.2)
client_socket.close()
gp.cleanup()
















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










