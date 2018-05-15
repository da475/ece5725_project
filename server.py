import bluetooth
import RPi.GPIO as gp
import pygame
import os
import math
import time


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

# FISH
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
    #water_level = MAX_LEVEL + MIN_LEVEL - water_level
 

    """   
    # display on the wall
    screen.fill(BLACK)
    rect = (0, 200-water_level, SCREEN_WIDTH, 40+water_level)       # x, y, width, height
    pygame.draw.rect(screen, BLUE, rect, 0)
    pygame.display.update()
    time.sleep(0.2)

    """

    ################  NEW CODE  #####################

    # display fish
    br1 = br1.move(speed)
    if br1.left < 0 or br1.right > FISH_WIDTH:
        speed[0] = -speed[0]
    
    if br1.top < 0 or br1.bottom > FISH_HEIGHT:
        speed[1] = -speed[1]

    screen.blit(fish , br1)
   


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
    text_surface = current_msg_font.render('FLOOD LEVEL', True, BLUE)
    rect = text_surface.get_rect(center=current_msg_pos)
    screen.blit(text_surface, rect)


    # display the current number 
    level = float(water_level / 600.0)
    number_str = str(level)
    text_surface = current_number_font.render(number_str, True, BLUE)
    rect = text_surface.get_rect(center = current_number_pos)
    screen.blit(text_surface, rect)


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


