# code combines charlie and sesnor code
# to glow up leds accordingly


import RPi.GPIO as gp
import time
from led_charlie import *

gp.setmode(gp.BCM)

# macros
MIN_DIST = 1000
MAX_DIST = 3000
MID_DIST = int((MIN_DIST + MAX_DIST) / 2)
OFFSET = int( (MAX_DIST - MIN_DIST) / 5 )

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

gp.setup(pin_quit, gp.IN, pull_up_down=gp.PUD_UP)
gp.setup(pin_ledR, gp.OUT)
gp.setup(pin_ledG, gp.OUT)
gp.setup(gp_trigger, gp.OUT)
gp.setup(gp_echo, gp.IN)

gp.setwarnings(False)

# setup PWM for the leds
# todo remove it later
p_red = gp.PWM(pin_ledR, 1)     # 1Hz freq
p_green = gp.PWM(pin_ledG, 1)     # 1Hz freq

# start with initial duty cycle for green and red LEDs
p_red.start(0)                  # start with 0% duty cycle
p_green.start(50)               # start with 100% duty cycle


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
        print ('dur in us is ', duration)
        

gp.add_event_detect(gp_echo, gp.BOTH, callback=gp26_cb, bouncetime=1)


############### SENSOR ########################


def main():
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

        # level 1
        if duration < MIN_DIST + OFFSET:
            charlie_obj.glow_led1()

        # level 2
        elif duration < MIN_DIST + (OFFSET*2):
            charlie_obj.glow_led2()

        # level 3
        elif duration < MIN_DIST + (OFFSET*3):
            charlie_obj.glow_led3()

        # level 4
        elif duration < MIN_DIST + (OFFSET*4):
            charlie_obj.glow_led4()

        # level 5
        elif duration < MIN_DIST + (OFFSET*5):
            charlie_obj.glow_led5()

        #default case
        else:
            print ('Out of range')

        if quit_signal == 1:
            break

    # cleanup code
    p_red.stop()
    p_green.stop()
    gp.cleanup()

main()


