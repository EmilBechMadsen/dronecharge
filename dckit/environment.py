from dckit.tasks.task import Task
from dckit.tasks.landing_task import LandingTask
from dckit.charger.charger_manager import ChargerManager
from dckit.drone_factory import DroneFactory
from dckit.tasks.movement_task import MovementTask
import logging


logger = logging.getLogger(__name__)


class Environment(object):
    #Private variables
    __chargerManager = None
    __droneFactory = None

    """
    """
    def __init__(self):
        super(Environment, self).__init__()
        self.frame_of_reference = None
        self.origin = None
        self.chargers = []
        self.__droneFactory = DroneFactory()
        self.__chargerManager = ChargerManager(self.__droneFactory)
        self.drones = []
        self.tasks = []

    def addTask(self, task):
        task.environment = self
        self.tasks.append(task)

    def setFrameOfReference(self, frameOfReference):
        self.frame_of_reference = frameOfReference

    def setOrigin(self, origin):
        self.origin = origin

    def addCharger(self, charger):
        self.chargers.append(charger)

    def addDrone(self, drone):
        drone.environment = self
        drone.setEnvironment(self)
        drone.initialize()
        self.__droneFactory.addDrone(drone)

    #def start(self, timeout=300):
    #    for drone in self.drones:
    #        drone.setEnvironment(self)
    #        drone.initialize()

    def getDrone(self, capabilities):
        return self.__droneFactory.getDrone()
        for drone in self.drones:
            if not drone.hasCapabilities(capabilities):
                caps = set(capabilities) - set(drone.capabilities)
                logger.info("Rejecting drone based on capabilities %s", caps)
                continue
            if not drone.isCharged():
                logger.info("Rejecting drone because it is not charged")
                continue

            capableDrones.append(drone)

        if len(capableDrones) == 0:
            return None
        else:
            return sorted(capableDrones, key=lambda x: len(x.capabilities))[0]

    def replaceDroneIfNeeded(self, drone, required_capabilities):
        if drone is None or drone.isBatteryLow():
            # dequeue a new drone
            drone = self.getDrone(required_capabilities)
        return drone
