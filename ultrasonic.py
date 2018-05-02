
import RPi.GPIO as gp
import time


######  GPIO  ###########

gp_trigger = 13
gp_echo = 26
gp.setmode(gp.BCM)
gp.setup(gp_trigger, gp.OUT)
gp.setup(gp_echo, gp.IN)

start_time = 0
duration = 0

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
gp.output(gp_trigger, gp.LOW)

while(1):

    # send the trigger pulse
    gp.output(gp_trigger, gp.HIGH)
    time.sleep(20/1000000.0)
    gp.output(gp_trigger, gp.LOW)

    # wait for 100ms
    time.sleep(0.1)

