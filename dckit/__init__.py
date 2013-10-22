
from dckit.environment import Environment

class DCKit(object):
	"""Main class that encapsulates everything

	"""

	environment = None
	drones = []

	def __init__(self):
		super(DCKit, self).__init__()

		self.environment = Environment()
		
	def add_drone(self, drone):
		drones.append(drone)

	def _main_loop(self):
		while True:
			# self.environment
			
			for drone in drones:
				drone.tick()
