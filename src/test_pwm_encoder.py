#!/usr/bin/env python

import sys
import time

import wiringpi2

from encoder_reader import EncoderReader
from ports import port_motor_left_forward, port_motor_right_forward, \
    port_motor_left_backward, port_motor_right_backward, \
    port_motor_left_pwm, port_motor_right_pwm, port_encoder_left_a, \
    port_encoder_left_b, port_encoder_right_a, port_encoder_right_b


# ./test_pwm_encoder.py 20 100
pwm_divisor = int(sys.argv[1])
pwm_range = int(sys.argv[2])

wiringpi2.pinMode(port_motor_left_pwm, wiringpi2.GPIO.PWM_OUTPUT)
wiringpi2.pinMode(port_motor_right_pwm, wiringpi2.GPIO.PWM_OUTPUT)
wiringpi2.pinMode(port_motor_left_forward, wiringpi2.GPIO.OUTPUT)
wiringpi2.pinMode(port_motor_right_forward, wiringpi2.GPIO.OUTPUT)

wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS)
wiringpi2.pwmSetRange(pwm_range)
wiringpi2.pwmSetClock(pwm_divisor)

# pwmFrequency in Hz = 19.2 MHz / pwmClock / pwmRange
frequency = 19200000 / pwm_divisor / pwm_range


print ("frequency={} Hz (divisor={}, range={})".format(frequency, pwm_divisor, pwm_range))

#encoderLeft = EncoderReader(port_encoder_left_a, port_encoder_left_b)
encoderRight = EncoderReader(port_encoder_right_a, port_encoder_right_b)

def shutdown():
    wiringpi2.pwmWrite(port_motor_left_pwm, 0)
    wiringpi2.pwmWrite(port_motor_right_pwm, 0)
    wiringpi2.digitalWrite(port_motor_left_backward, wiringpi2.GPIO.LOW)
    wiringpi2.digitalWrite(port_motor_left_forward, wiringpi2.GPIO.LOW)
    wiringpi2.digitalWrite(port_motor_right_backward, wiringpi2.GPIO.LOW)
    wiringpi2.digitalWrite(port_motor_right_forward, wiringpi2.GPIO.LOW)

    wiringpi2.digitalWrite(port_motor_left_forward, wiringpi2.GPIO.LOW)
    wiringpi2.digitalWrite(port_motor_right_forward, wiringpi2.GPIO.LOW)

try:
    percentage = 0
    previousCounterLeft = 0
    previousCounterRight = 0
    while percentage < 100:
        pwm_value = pwm_range * percentage / 100
        wiringpi2.digitalWrite(port_motor_left_forward, wiringpi2.GPIO.HIGH)
        wiringpi2.digitalWrite(port_motor_right_forward, wiringpi2.GPIO.HIGH)
        wiringpi2.pwmWrite(port_motor_left_pwm, pwm_value)
        wiringpi2.pwmWrite(port_motor_right_pwm, pwm_value)

        time.sleep(1)

        #counterLeft = encoderLeft.getCounterValue()
        #stepsLeft = counterLeft - previousCounterLeft
        #previousCounterLeft = counterLeft
        counterLeft=0
        stepsLeft=0
        
        counterRight = encoderRight.getCounterValue()
        stepsRight = counterRight - previousCounterRight
        previousCounterRight = counterRight
        
        
        print ("percentage={} counterLeft={} stepsLeft={} counterRight={} stepsRight={}".format(percentage, counterLeft, stepsLeft, counterRight, stepsRight))
        
#         if counterLeft < -10 or counterLeft > 10:
#             print ("detected movement at {}".format(percentage))
#             break
        percentage += 1
        
    shutdown()

except (KeyboardInterrupt, SystemExit):
    print "caught exception, exiting..."
    shutdown()
    sys.exit(1)
