class Crazyflie(Drone):
	"""docstring for Crazyflie"""
	def __init__(self):
		super(Crazyflie, self).__init__()
	
	def initialize(self):
		pass

	def set_heading(self, heading):
		assert heading >= 0.0 and heading < 360.0
		# do something

	def get_heading(self):
		return 360.0

	def set_forward_speed(self, speed):
		# speed is normalized to 0.0 - 1.0
		pass

	def set_climb_rate(self, climb_rate):
		# climb_rate is normalized to 0.0 - 1.0
		pass

	def noop(self):
		# hover in place
		pass

	def get_battery_level(self):
		# return battery level normalized to 0.0 - 1.0
		self.battery = 10

	def get_position(self):
		# return drone's position in the environment's coordinate system
		raise NotImplementedError("Please Implement this method")
	
	def get_drone_diameter(self):
		# return drone size in the environment's coordinate system
		pass	

