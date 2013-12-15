from dckit.tasks.task import Task
from dckit.tasks.landing_task import LandingTask
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

    def stopAllDrones(self):
        self.__droneManager.stopAllDrones()

    #def start(self, timeout=300):
    #    for drone in self.drones:
    #        drone.setEnvironment(self)
    #        drone.initialize()

    def replaceDroneIfNeeded(self, drone, required_capabilities):
        if drone is None or drone.isBatteryLow():
            # dequeue a new drone
            drone = self.__droneManager.getDrone(required_capabilities)
        return drone

    def resetTaskTree(self, taskRoot):
        for subtask in taskRoot.subtasks:
            subtask.state = TaskState.READY
            self.resetTasktree(subtask)
        taskRoot.state = TaskState.READY

    def deleteTaskTree(self, taskRoot):
        self.tasks.remove(taskRoot)

    def getAllDrones(self):
        return self.__droneManager.getAllDrones()