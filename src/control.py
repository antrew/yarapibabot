import logging
from math import atan2
import math
from threading import Thread
from time import time, sleep

from log_data_set import LogDataSet
from motor import Motor
from mpu6050 import MPU6050
from ports import port_motor_left_backward, port_motor_left_forward, port_motor_right_backward, port_motor_right_forward, \
    port_motor_left_pwm, port_motor_right_pwm


class ControlThread(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.angle = 0
        self.K = 0.98
        self.logDataSetBuffer = []

        self.Kp = config.config.as_float('Kp')
        self.Ki = config.config.as_float('Ki')
        self.Kd = config.config.as_float('Kd')
        self.set_point = config.config.as_float('set_point')
        self.disable_motors = config.config.as_bool('disable_motors')
        
        self.integral_error = 0
        self.last_error = 0
        self.motor_left = Motor("L", port_motor_left_pwm, port_motor_left_backward, port_motor_left_forward)
        self.motor_right = Motor("R", port_motor_right_pwm, port_motor_right_backward, port_motor_right_forward)
        
        self.accelerometer = MPU6050()

        self.last_time = time()

        self.logger = logging.getLogger(__name__)

        self.setDaemon(True)
        self.latest_sensor = 0
        
        self.logger.info('Initialized ControlThread with the following settings')
        self.logger.info('disable_motors={}'.format(self.disable_motors))
        self.logger.info('set_point={:1.2f}'.format(self.set_point))
        self.logger.info('Kp={:1.1f}'.format(self.Kp))
        self.logger.info('Ki={:1.1f}'.format(self.Ki))
        self.logger.info('Kd={:1.1f}'.format(self.Kd))


    def run(self):
        while True:
            self.perform_one_step()

    def perform_one_step(self):
        # create an object for logging the current sensors' data and current control data
        currentLogDataSet = LogDataSet()
        
        # read sensors
        axes = self.accelerometer.getAxes(True)
        self.latest_sensor = axes
        z = axes['z']
        x = axes['x']
        accelerometerAngle = atan2(-x, -z)
        # read gyroscope
        gyroscopeRate = -axes['gy'] / 180 * math.pi
        
        # log the values from the sensors
        currentLogDataSet.setSensorsValues(axes, gyroscopeRate)
        
        # calculate dt based on the current time and the previous measurement time
        now = time()
        dt = now - self.last_time
        self.dt = dt
        self.last_time = now 
        
        # complementary filter
        self.angle = self.K * (self.angle + gyroscopeRate * dt) + (1 - self.K) * accelerometerAngle

        # PID
        error = self.angle - self.set_point
        self.integral_error += error * dt
        differential_error = (error - self.last_error) / dt
        self.last_error = error
        
        u = self.Kp * error + self.Ki * self.integral_error + self.Kd * differential_error
        self.u = u
        
        # log the calculated control values
        currentLogDataSet.setControlValues(accelerometerAngle, self.angle, error, self.integral_error, differential_error, u, dt)
        # append the current logDataSet object to the logging-buffer
        self.logDataSetBuffer.append(currentLogDataSet)
        # limit the size of the buffer
        if len(self.logDataSetBuffer) > 500: 
            del self.logDataSetBuffer[0]
            
        self.logger.debug(
            'x={:5.2f} z={:5.2f} gy={:7.2f} accelAngle={:5.2f} gyrAngle={:5.2f} angle={:5.2f} e={:5.2f} ie={:5.2f} de={:5.2f} u={:5.2f} dt={:3.0f}'
                .format(
                    x, z, gyroscopeRate, accelerometerAngle, gyroscopeRate * dt, self.angle, error, self.integral_error, differential_error, u, dt * 1000))
        
        # control the motors
        if not self.disable_motors:
            self.motor_left.set_value(u, dt)
            self.motor_right.set_value(u, dt)

        #sleep(10. / 1000.)
    
    # return a copy of the current logDataSetBuffer and then empty the logDataSetBuffer     
    def getLogDataSetBuffer(self):
        # TODO synchronize this with the control loop thread
        data = self.logDataSetBuffer
        self.logDataSetBuffer=[]
        return data
