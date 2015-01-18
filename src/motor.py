import logging

import wiringpi2


class Motor:
    def __init__(self, backward_port, forward_port):
        self.backward_port = backward_port
        self.forward_port = forward_port
        # initialize Raspberry Pi ports for output
        wiringpi2.pinMode(backward_port, wiringpi2.GPIO.OUTPUT)
        wiringpi2.pinMode(forward_port, wiringpi2.GPIO.OUTPUT)
        
        # -1, 0, 1
        self.current_direction = 0
        
        self.integral_error = 0
        self.logger = logging.getLogger(__name__)
        
    def set_value(self, new_value, dt):
        # limit the target value to the range -1 .. 1
        if new_value > 1:
            new_value = 1
        if new_value < -1:
            new_value = -1
        
        self.target_value = new_value
        
        # current error
        error = self.current_direction - self.target_value 
        # integral error
        self.integral_error += error * dt

        if self.target_value > 0:
            if self.integral_error > 0:
                self.current_direction = 0
            else:
                self.current_direction = 1
        elif self.target_value < 0:
            if self.integral_error < 0:
                self.current_direction = 0
            else:
                self.current_direction = -1
        else:
            self.current_direction = 0

        self.logger.debug("target_value={} error={} integral_error={} direction={}".format(self.target_value, error, self.integral_error, self.current_direction))

        if self.current_direction > 0:
            # forward
            wiringpi2.digitalWrite(self.backward_port, wiringpi2.GPIO.LOW)
            wiringpi2.digitalWrite(self.forward_port, wiringpi2.GPIO.HIGH)
        elif self.current_direction < 0:
            # backward
            wiringpi2.digitalWrite(self.backward_port, wiringpi2.GPIO.HIGH)
            wiringpi2.digitalWrite(self.forward_port, wiringpi2.GPIO.LOW)
        else:
            wiringpi2.digitalWrite(self.backward_port, wiringpi2.GPIO.LOW)
            wiringpi2.digitalWrite(self.forward_port, wiringpi2.GPIO.LOW)
