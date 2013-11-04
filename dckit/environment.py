

class Environment(object):
    """
    """

    # coordinatesystem
    # location
    #
    frame_of_reference = None
    origin = None
    chargers = []
    drones = []

    def __init__(self, arg=None):
        super(Environment, self).__init__()
        self.arg = arg

    def set_frame_of_reference(self, frameOfReference):
        self.frame_of_reference = frameOfReference

    def set_origin(self, origin):
        self.origin = origin

    def add_charger(self, charger):
        self.chargers.append(charger)

    def add_drone(self, drone):
        self.drones.append(drone)

    def start(self, timeout=300):
        for drone in self.drones:
            drone.setEnvironment(self)
            drone.initialize()


