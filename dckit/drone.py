class Drone(object):
    """Base class for drone drivers

    """

    capabilities = [""]

    name = "Generic Drone"
    environment = None
    starting_position = None
    position = None
    target = None
    batterly_level = None

    def __init__(self, name, environment=None):
        super(Drone, self).__init__()
        self.name = name
        self.environment = environment

    def initialize(self):
        self.starting_position = self.get_position()
        self.position = self.starting_position

    def setEnvironment(self, environment):
        self.environment = environment

    def move(self, position, x=None, y=None, z=None):
        if len(position) == 3:
            self.target = position
        elif x is not None and y is not None and z is not None:
            self.target = (x, y, z)
        else:
            raise ValueError("Provide either position \
                tuple or separate positions")

    def moveRelative(self, position=None, x=None, y=None, z=None):
        pass

    # Abstract functions

    def getBatteryLevel(self):
        raise NotImplementedError("Please Implement this method")

    def getPosition(self):
        raise NotImplementedError("Please Implement this method")
