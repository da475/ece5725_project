import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

led_x1 = 21
led_x2 = 20
led_x3 = 16
led_x4 = 23
delay = 2

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

"""
co = charlie()
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
"""

gp.cleanup()


