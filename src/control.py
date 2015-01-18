from threading import Thread
from motor import Motor
from ports import port_motor_left_backward, port_motor_left_forward
from time import time
from adxl345 import ADXL345
from math import atan2

class ControlThread(Thread):
    def __init__(self, group=None, target=None, name=None,
        args=(), kwargs=None, verbose=None):
        Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self.angle = 0
        self.K = 0.98

        # TODO find better values        
        self.Kp = 0.5
        self.Ki = 0
        self.Kd = 0
        
        self.set_point = 0
        
        self.integral_error = 0
        self.last_error = 0
        self.motor = Motor(port_motor_left_backward, port_motor_left_forward)
        
        self.accelerometer = ADXL345()

    def run(self):
        # TODO read sensors
        axes = self.accelerometer.getAxes(True)
        z = axes['z']
        x = axes['x']
        accelerometerAngle = atan2(x, z)
        # TODO read gyroscope
        gyroscopeRate = 0
        
        # TODO calculate dt based on the current time and the previous measurement time
        now = time()
        dt = now - self.last_time
        self.last_time = now 
        
        # complementary filter
        self.angle = self.K * (self.angle + gyroscopeRate * dt) + (1 - self.K) * accelerometerAngle

        # TODO PID
        error = self.set_point - self.angle
        self.integral_error += error * dt
        differential_error = (error - self.last_error) / dt
        self.last_error = error
        
        u = self.Kp * error + self.Ki * self.integral_error + self.Kd * differential_error
        
        # TODO control the motor
        self.motor.set_value(u, dt)
        
