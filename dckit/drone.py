from threading import Thread
import time
import logging


logger = logging.getLogger(__name__)


class Drone(object):
    """Base class for drone drivers

    """

    def __init__(self, name, environment=None):
        super(Drone, self).__init__()
        self.name = name
        self.environment = environment
        self.starting_position = None
        self.position = (0, 0, 0)
        self.target = (0, 0, 0)
        self.battery_level = 1.0
        self.low_battery_level = 0.1
        self.capabilities = []
        self.charger = None

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

    def isBatteryLow(self):
        return self.low_battery_level * 2.0 >= self.battery_level

    def hasCapabilities(self, capabilities):
        required_capabilities = set(capabilities)
        available_capabilities = set(self.capabilities)

        return required_capabilities.issubset(available_capabilities)

    def getState(self):
        pass

    def setState(self):
        pass

    def startControlLoop(self):
        self.thread = Thread(group=None, target=self.controlLoop).start()

    def controlLoop(self):
        logger.error("Control Loop not implemented!")
        pass

    # Abstract functions
    def getBatteryLevel(self):
        raise NotImplementedError("Please Implement this method")

    def getPosition(self):
        raise NotImplementedError("Please Implement this method")

    def isCharged(self):
        raise NotImplementedError("Please implement this method")
