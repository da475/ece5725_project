import bluetooth
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


############ PYGAME #############

MIN_LEVEL = 980
MAX_LEVEL = 3000
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
size = SCREEN_WIDTH, SCREEN_HEIGHT
BLACK = (0,0,0)
BLUE = (0, 0, 255)
rect = (0, 200, SCREEN_WIDTH, 40)       # x, y, width, height

pygame.init()
screen = pygame.display.set_mode(size)

screen.fill(BLACK)
pygame.draw.rect(screen, BLUE, rect, 0)

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
    water_level = water_level - MIN_LEVEL
    water_level = int(water_level / 50)
    water_level = 20
    print ('water level is ', water_level)
    
    # display on the wall
    screen.fill(BLACK)
    rect = (0, 200-water_level, SCREEN_WIDTH, 40+water_level)       # x, y, width, height
    pygame.draw.rect(screen, BLUE, rect, 0)
    pygame.display.update()
    time.sleep(0.2)


# close the sockets
client_socket.close()
server_socket.close()
gp.cleanup()



