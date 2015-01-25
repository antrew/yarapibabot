import logging
from math import atan2
from threading import Thread
from time import time, sleep

from motor import Motor
from mpu6050 import MPU6050
from ports import port_motor_left_backward, port_motor_left_forward


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
        
        # self.accelerometer = ADXL345()
        self.accelerometer = MPU6050()

        self.last_time = time()

        self.logger = logging.getLogger(__name__)

        self.setDaemon(True)

    def run(self):
        while True:
            self.perform_one_step()

    def perform_one_step(self):
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
        
        self.logger.debug('u={} dt={}'.format(u, dt * 1000))
        
        # TODO control the motor
        self.motor.set_value(u, dt)

        sleep(10. / 1000.)
