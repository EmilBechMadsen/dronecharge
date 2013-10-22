class Drone(object):
	"""Base class for drone drivers

	"""

	name = "Generic Drone"
	environment = None
	starting_position = None
	position = None
	target = None
	batterly_level = None

	def __init__(self, name, environment):
		super(Drone, self).__init__()
		self.name = name

	def initialize(self):
		self.starting_position = self.get_position()
		self.position = self.starting_position
	
	def set_environment(self, environment):
		self.environment = environment

	def move(self, position=None, x=None, y=None, z=None):
		if len(position) == 3:
			self.target = position
		elif x is not None and y is not None and z is not None:
			self.target = (x, y, z)
		else:
			raise ValueError("Provide either position tuple or separate positions")

	def move_relative(self, position=None, x=None, y=None, z=None):
		pass

	# Abstract functions

	def get_battery_level(self):
		raise NotImplementedError("Please Implement this method")

	def get_position(self):
		raise NotImplementedError("Please Implement this method")
