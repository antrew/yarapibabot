import logging
import math

import wiringpi2


class Motor:
    def __init__(self, name, pwm_port, backward_port, forward_port):
        self.name = name
        self.pwm_port = pwm_port
        self.backward_port = backward_port
        self.forward_port = forward_port
        self.backward_value = 0
        self.forward_value = 0
        # initialize Raspberry Pi ports for output
        wiringpi2.pinMode(self.pwm_port, wiringpi2.GPIO.PWM_OUTPUT)
        wiringpi2.pinMode(self.backward_port, wiringpi2.GPIO.OUTPUT)
        wiringpi2.pinMode(self.forward_port, wiringpi2.GPIO.OUTPUT)
        
        wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS);
        self.pwm_range = 100
        wiringpi2.pwmSetRange(self.pwm_range)
        wiringpi2.pwmSetClock(1)
        # pwmFrequency in Hz = 19.2 MHz / pwmClock / pwmRange
        self.logger = logging.getLogger(__name__)
        
    def set_value(self, target, dt):
        # limit the target value to the range -1 .. 1
        if target > 1:
            target = 1
        if target < -1:
            target = -1
        
        # set direction
        if target > 0:
            # forward_value
            backward_value = wiringpi2.GPIO.LOW
            forward_value = wiringpi2.GPIO.HIGH
        elif target < 0:
            # backward_value
            backward_value = wiringpi2.GPIO.HIGH
            forward_value = wiringpi2.GPIO.LOW
        else:
            backward_value = wiringpi2.GPIO.LOW
            forward_value = wiringpi2.GPIO.LOW

        if self.backward_value != backward_value:
            wiringpi2.digitalWrite(self.backward_port, backward_value)
        if self.forward_value != forward_value:
            wiringpi2.digitalWrite(self.forward_port, forward_value)
        self.backward_value = backward_value
        self.forward_value = forward_value

        # set power
        if target < 0:
            target = -target
        power = int(self.pwm_range * target)
        wiringpi2.pwmWrite(self.pwm_port, power)

        self.logger.debug("{}: target={:5.2f} backward_value={:1d} forward_value={:1d} power={:4d}/{:4d}".format(self.name, target, backward_value, forward_value, power, self.pwm_range))
