from dckit.tasks.task import Task
from dckit.tasks.landing_task import LandingTask
from dckit.charger.charger_manager import ChargerManager
from dckit.drone_manager import DroneManager
from dckit.tasks.movement_task import MovementTask
import logging
from dckit.tasks.task import TaskState


logger = logging.getLogger(__name__)

class Environment(object):
    #Private variables
    __droneManager = None

    """
    """
    def __init__(self):
        super(Environment, self).__init__()
        self.frame_of_reference = None
        self.origin = None
        self.__droneManager = DroneManager()
        self.drones = []
        self.tasks = []

    def addTask(self, task):
        task.environment = self
        self.tasks.append(task)

    def setFrameOfReference(self, frameOfReference):
        self.frame_of_reference = frameOfReference

    def setOrigin(self, origin):
        self.origin = origin

    def addDrone(self, drone):
        drone.setEnvironment(self)
        drone.initialize()
        drone.startControlLoop()
        self.__droneManager.addDrone(drone)

    #def start(self, timeout=300):
    #    for drone in self.drones:
    #        drone.setEnvironment(self)
    #        drone.initialize()

    def replaceDroneIfNeeded(self, drone, required_capabilities):
        logger.info("CHECKING DRONE BATTERY")
        if drone is None or drone.isBatteryLow():
            if drone is not None:
                logger.info("DRONE BATTERY IS LOW ON DRONE %s: %s", drone.name, drone.battery_level)
            # dequeue a new drone
            drone = self.__droneManager.getDrone(required_capabilities)
        return drone

    def resetTaskTree(self, taskRoot):
        for subtask in task.subtasks:
            subtask.state = TaskState.READY
            resetTask(subtask)
        taskRoot.state = TaskState.READY

    def deleteTaskTree(self, taskRoot):
        self.tasks.remove(taskRoot)

    def getAllDrones(self):
        return self.__droneManager.getAllDrones()