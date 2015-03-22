#!/usr/bin/env python

import sys
import time

import wiringpi2

from ports import port_motor_left_forward, port_motor_right_forward, \
    port_motor_left_pwm, port_motor_right_pwm


pwm_divisor = int(sys.argv[1])
pwm_range = int(sys.argv[2])
percentage = int(sys.argv[3])

wiringpi2.pinMode(port_motor_left_pwm, wiringpi2.GPIO.PWM_OUTPUT)
wiringpi2.pinMode(port_motor_right_pwm, wiringpi2.GPIO.PWM_OUTPUT)
wiringpi2.pinMode(port_motor_left_forward, wiringpi2.GPIO.OUTPUT)
wiringpi2.pinMode(port_motor_right_forward, wiringpi2.GPIO.OUTPUT)

wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS)
wiringpi2.pwmSetRange(pwm_range)
wiringpi2.pwmSetClock(pwm_divisor)

# pwmFrequency in Hz = 19.2 MHz / pwmClock / pwmRange
frequency = 19200000 / pwm_divisor / pwm_range
pwm_value = pwm_range * percentage / 100

print ("frequency={} Hz (divisor={}, range={}, value={})".format(frequency, pwm_divisor, pwm_range, pwm_value))

for i in range(1, 5):
    print "on"
    wiringpi2.digitalWrite(port_motor_left_forward, wiringpi2.GPIO.HIGH)
    wiringpi2.digitalWrite(port_motor_right_forward, wiringpi2.GPIO.HIGH)
    wiringpi2.pwmWrite(port_motor_left_pwm, pwm_value)
    wiringpi2.pwmWrite(port_motor_right_pwm, pwm_value)

    time.sleep(2)
    print "off"
    wiringpi2.pwmWrite(port_motor_left_pwm, 0)
    wiringpi2.pwmWrite(port_motor_right_pwm, 0)
    time.sleep(2)

wiringpi2.digitalWrite(port_motor_left_forward, wiringpi2.GPIO.LOW)
wiringpi2.digitalWrite(port_motor_right_forward, wiringpi2.GPIO.LOW)
