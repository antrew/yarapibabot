#!/usr/bin/env python

from bottle import route, run
from adxl345 import ADXL345

@route('/hello')
def hello():
    return "Hello World!"

@route('/accel')
def accel():
    adxl345 = ADXL345()
     
    axes = adxl345.getAxes(True)
    
#     return {'status':'online', 'servertime':time.time()}
    
#     response = "ADXL345 on address 0x%x:" % (adxl345.address)
#     response += "   x = %.3fG" % (axes['x'])
#     response += "   y = %.3fG" % (axes['y'])
#     response += "   z = %.3fG" % (axes['z'])
    response = axes
    return response

run(host='0.0.0.0', port=8080, debug=True)
