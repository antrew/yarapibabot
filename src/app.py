#!/usr/bin/env python
import logging
from multiprocessing.process import Process
import sys
import time

from bottle import Bottle
from control import ControlThread


logging.basicConfig(level=logging.DEBUG)

# start the main control thread
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
    axes = controlThread.latest_sensor
    
    response = {'axes': axes, 'something':'else'}
    
    return response

bottle_process = Process(target=web_server.run, kwargs=dict(host='0.0.0.0', port=8080, debug=True))
bottle_process.daemon = True
bottle_process.start()

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print "caught exception, exiting..."
    sys.exit(1)
