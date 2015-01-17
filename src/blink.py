#!/usr/bin/env python

import wiringpi2
import time
import sys

port=int(sys.argv[1])

#wiringpi2.wiringPiSetup() # For sequential pin numbering, one of these MUST be called before using IO functions
#wiringpi2.wiringPiSetupSys() # For /sys/class/gpio with GPIO pin numbering
#wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering

wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering

wiringpi2.pinMode(port, wiringpi2.GPIO.OUTPUT)

print ('blinking with port {}'.format(port))

for i in range(1, 5):
    print "on"
    wiringpi2.digitalWrite(port, wiringpi2.GPIO.HIGH)
    time.sleep(0.5)
    print "off"
    wiringpi2.digitalWrite(port, wiringpi2.GPIO.LOW)
    time.sleep(0.5)
