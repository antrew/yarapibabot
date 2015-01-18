#!/usr/bin/env python
import logging

from control import ControlThread


logging.basicConfig(level=logging.DEBUG)

# start the main control thread
controlThread = ControlThread()
controlThread.start()

# TODO start the web server for debugging
# - accelerometer values
# - gyroscope values
# - dt
# - error in ControlThread (current, integral, differential)
# - error, direction, target_value in Motor
# TODO display this all in multiple charts in plotter.py

controlThread.join()
