#!/usr/bin/env python
from control import ControlThread


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
