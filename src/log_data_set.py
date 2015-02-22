# This class defines the control data that we want to keep for debugging purposes
class LogDataSet():
	def __init__(self):
		# sensors' values
		self.sensors = LogSensorsData()
		# control values
		self.control = LogControlData()
	
	def setSensorsValues(self, axes, gyroscopeRate):
		# set sensors' values
		self.sensors = axes
		self.sensors["gyroscopeRate"] = gyroscopeRate
		#self.sensors.setSensorsValues(axes, gyroscopeRate)
		
	def setControlValues(self, accelerometerAngle, angle, error, integral_error, differential_error, u, dt):
		# set the control values
		self.control.setControlValues(accelerometerAngle, angle, error, integral_error, differential_error, u, dt)
		
		
class LogSensorsData:
	def __init__(self):
		# sensors' values
		self.axes = None
		self.gyroscopeRate = None
		
class LogControlData:
	def __init__(self):
		# control values
		self.accelerometerAngle = None
		self.angle = None
		self.error = None 
		self.integral_error = None 
		self.differential_error = None 
		self.u = None
		self.dt = None
	
	def setControlValues(self, accelerometerAngle, angle, error, integral_error, differential_error, u, dt):
		# set the control values
		self.accelerometerAngle = accelerometerAngle
		self.angle = angle
		self.error = error 
		self.integral_error = integral_error 
		self.differential_error = differential_error 
		self.u = u
		self.dt = dt