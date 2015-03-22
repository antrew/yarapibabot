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

        # experimentally found values (use test_pwm.py):
        # frequency = 19200 (not hearable)
        # divisor = 2
        # range = 500
        # dead zone <= 53%
        self.mapping_u = [0, 1, 100]
        #self.mapping_pwm = [0, 53, 100]
        self.mapping_pwm = [0, 53, 100]
        
        wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS);
        self.divisor = 2
        self.pwm_range = 1000
        wiringpi2.pwmSetRange(self.pwm_range)
        wiringpi2.pwmSetClock(self.divisor)
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
        
        # find interpolation range
        for idx, val in enumerate(self.mapping_u):
            print idx, val
            if val > target*100.0:
                # found
                break
        if idx <= 0:
            idx = 1
        if idx > len(self.mapping_u):
            idx = len(self.mapping_u)
        # interpolate
        u1 = float(self.mapping_u[idx - 1])
        u2 = float(self.mapping_u[idx])
        p1 = float(self.mapping_pwm[idx - 1])
        p2 = float(self.mapping_pwm[idx])
        power_percent = p1 + (target * 100.0 - u1) * (p2 - p1) / (u2 - u1)
        self.logger.debug("{}: target={} idx={} u1={:5.2f} u2={:1f} p1={:1f} p2={:4f}".format(self.name, idx, target, u1, u2, p1, p2))
        
        # scale to pwm_range
        power = int(self.pwm_range * power_percent / 100)
        wiringpi2.pwmWrite(self.pwm_port, power)

        self.logger.debug("{}: target={:5.3f} backward_value={:1d} forward_value={:1d} power={:2.0f} %={:4d}/{:4d}".format(self.name, target, backward_value, forward_value, power_percent, power, self.pwm_range))
