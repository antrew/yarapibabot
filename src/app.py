#!/usr/bin/env python
import logging
import sys
from threading import Thread
import time

import wiringpi2

from bottle import Bottle, response
from control import ControlThread
import ports
from json import dumps


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# start the main control thread
global controlThread

controlThread = ControlThread()
controlThread.daemon = True
controlThread.start()

# TODO start the web server for debugging
# - accelerometer values
# - gyroscope values
# - dt
# - error in ControlThread (current, integral, differential)
# - error, direction, target_value in Motor
# TODO display this all in multiple charts in plotter.py


web_server = Bottle()

@web_server.route('/sensors')
def sensors():
    global controlThread
    logDataSetBuffer = controlThread.getLogDataSetBuffer()
    # return the logDataSetBuffer's latest state
    response.content_type = "application/json"    
    return dumps(logDataSetBuffer, default=lambda o: o.__dict__)

bottle_thread = Thread(target=web_server.run, kwargs=dict(host='0.0.0.0', port=8080, debug=True))
bottle_thread.daemon = True
bottle_thread.start()

try:
    while True:
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    print "caught exception, exiting..."
    wiringpi2.pwmWrite(ports.port_motor_left_pwm, 0)
    wiringpi2.pwmWrite(ports.port_motor_right_pwm, 0)
    wiringpi2.digitalWrite(ports.port_motor_left_backward, wiringpi2.GPIO.LOW)
    wiringpi2.digitalWrite(ports.port_motor_left_forward, wiringpi2.GPIO.LOW)
    wiringpi2.digitalWrite(ports.port_motor_right_backward, wiringpi2.GPIO.LOW)
    wiringpi2.digitalWrite(ports.port_motor_right_forward, wiringpi2.GPIO.LOW)

    sys.exit(1)
