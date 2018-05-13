################
import bluetooth
import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

# macros
MIN_DIST = 990
MAX_DIST = 3000
MID_DIST = int((MIN_DIST + MAX_DIST) / 2)

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

        if(MIN_DIST<=duration<=MAX_DIST):
            duration = int(duration)

        elif(duration>MAX_DIST):
            duration = MAX_DIST

        else:
            duration = MIN_DIST
        print ('dur in us is ', duration)
        

gp.add_event_detect(gp_echo, gp.BOTH, callback=gp26_cb, bouncetime=1)


############### SENSOR ########################

gp.output(gp_trigger, gp.LOW)

while(1):

    # send the trigger pulse
    gp.output(gp_trigger, gp.HIGH)
    time.sleep(20/1000000.0)
    gp.output(gp_trigger, gp.LOW)

    # wait for 100ms
    time.sleep(0.1)

    # control the LEDs
    if duration > MID_DIST:
        # flag green signal
        #p_green.ChangeFrequency(0.6)
        p_green.ChangeDutyCycle(50)
        p_red.ChangeDutyCycle(0)
    else:
        # flag red signal
        #p_green.ChangeFrequency(0.6)
        p_red.ChangeDutyCycle(50)
        p_green.ChangeDutyCycle(0)

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
p_red.stop()
p_green.stop()
gp.cleanup()


