

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

    def setFrameOfReference(self, frameOfReference):
        self.frame_of_reference = frameOfReference

    def setOrigin(self, origin):
        self.origin = origin

    def addCharger(self, charger):
        self.chargers.append(charger)

    def addDrone(self, drone):
        self.drones.append(drone)

    def start(self, timeout=300):
        for drone in self.drones:
            drone.setEnvironment(self)
            drone.initialize()

    def getDrone(self, capabilities):
        capableDrones = [drone for drone in self.drones if drone.hasCapabilities(capabilities) and drone.isCharged]
        if len(capableDrones) == 0:
            return None
        else:
            return sorted(capableDrones, lambda x: len(x.capabilities))[0]
