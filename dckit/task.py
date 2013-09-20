class Task(object):
	"""Top level task class for defining "jobs" for the drones
	"""
	def __init__(self, arg):
		super(Task, self).__init__()
		self.arg = arg
