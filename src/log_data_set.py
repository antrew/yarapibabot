# This class defines the control data that we want to keep for debugging purposes
class LogDataSet():
	def __init__(self):
		# sensors' values
		self.x = None
		self.z = None
		self.gyroscopeRate = None
		# control values
		self.accelerometerAngle = None
		self.angle = None
		self.error = None 
		self.integral_error = None 
		self.differential_error = None 
		self.u = None
		self.dt = None
	
	def setSensorsValues(self, x, z, gyroscopeRate):
		# set sensors' values
		self.x = x
		self.z = z
		self.gyroscopeRate = gyroscopeRate
		
	def setControlValues(self, accelerometerAngle, angle, error, integral_error, differential_error, u, dt):
		# set the control values
		self.accelerometerAngle = accelerometerAngle
		self.angle = angle
		self.error = error 
		self.integral_error = integral_error 
		self.differential_error = differential_error 
		self.u = u
		self.dt = dt