from dckit.charger.charger_manager import ChargerManager
from dckit.drone_factory import DroneFactory

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
    
    #Private variables
    __chargerManager = None
    __droneFactory = None

    def __init__(self, arg=None):
        super(Environment, self).__init__()
        self.arg = arg
        self.__droneFactory = DroneFactory()
        self.__chargerManager = ChargerManager(self.__droneFactory)

    def setFrameOfReference(self, frameOfReference):
        self.frame_of_reference = frameOfReference

    def setOrigin(self, origin):
        self.origin = origin

    def addCharger(self, charger):
        self.chargers.append(charger)

    def addDrone(self, drone):
        drone.setEnvironment(self)
        drone.initialize()
        self.__droneFactory.addDrone(drone)

    #def start(self, timeout=300):
    #    for drone in self.drones:
    #        drone.setEnvironment(self)
    #        drone.initialize()

    def getDrone(self, capabilities):
        return self.__droneFactory.getDrone()
