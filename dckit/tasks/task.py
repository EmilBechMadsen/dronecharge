from dckit.enum import Enum
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskState(Enum):
    READY = 0
    EXECUTING = 1
    COMPLETE = 2


class Task(object):
    """Top level task class for defining "jobs" for the drones
    """

    def __init__(self, name="Task", environment=None):
        super(Task, self).__init__()

        self.name = name
        self.drone = None
        self.subtasks = []
        self.state = TaskState.READY
        self.required_capabilities = []
        self.environment = environment

    def start(self):
        self.state = TaskState.EXECUTING

    def isComplete(self):
        pass

    def setDrone(self, drone):
        self.drone = drone

    def setCapabilities(self, capabilities):
        self.required_capabilities = capabilities

    def addSubtask(self, task):
        self.subtasks.append(task)

    def accumulateCapabilities(self):
        if len(self.subtasks) == 0:
            return set(self.required_capabilities)

        self.required_capabilities = set(self.required_capabilities)

        for subtask in self.subtasks:
            caps = subtask.accumulateCapabilities()
            self.required_capabilities = self.required_capabilities.union(caps)

        return self.required_capabilities

    def evaluate(self):
        currentSubtask = self.getCurrentSubtask()
        if currentSubtask is None:
            if self.isComplete():
                self.state = TaskState.COMPLETE

            return

        # currentSubtask can be the state directly
        if currentSubtask == TaskState.COMPLETE:
            self.state = TaskState.COMPLETE
            return

        if currentSubtask.state == TaskState.READY:
            drone = self.drone
            logger.debug(drone)
            # TODO: or DRONE DOES NOT HAVE SUFFICIENT POWER
            if drone is None or drone.isBatteryLow():
                drone = self.environment.getDrone(self.required_capabilities)
                if drone is None: # IF IT'S STILL NONE, WE HAVE TO WAIT (BY TRYING AGAIN UNTILL ONE IS AVAILABLE)
                    return

                # insert the charging subtree for the current drone
                # insert move command for the new drone

            self.state = TaskState.EXECUTING
            currentSubtask.setDrone(drone)
            self.setDrone(drone)

            currentSubtask.start()
        else:
            currentSubtask.evaluate()

    def getCurrentSubtask(self):
        """
        Returns: - (Task) first subtask that is either ready or executing
                 - None if there are no subtasks defined
                 - TaskState.COMPLETE if all subtasks are complete
        """
        if len(self.subtasks) == 0:
            return None

        for subtask in self.subtasks:
            currentSubtask = subtask.getCurrentSubtask()
            # No children, not complete yet
            if currentSubtask is None and subtask.state != TaskState.COMPLETE:
                # Must be about to execute.
                self.state = TaskState.EXECUTING
                return subtask

            if subtask.state == TaskState.COMPLETE or \
                    currentSubtask == TaskState.COMPLETE:
                continue

            ready = currentSubtask.state == TaskState.READY
            executing = currentSubtask.state == TaskState.EXECUTING

            if ready or executing:
                # Must be about to execute.
                self.state = TaskState.EXECUTING
                return currentSubtask

        # Entire subtree complete means this is complete.
        self.state = TaskState.COMPLETE
        return TaskState.COMPLETE

    def __repr__(self):
        ret = "<Task (" + str(id(self)) + "): \n" + \
            "    Drone: " + str(self.drone) + " \n" + \
            "    Subtasks: " + str(self.subtasks) + " \n" + \
            "    State: " + str(self.state) + " \n" + \
            "    Capabilities: " + str(self.required_capabilities) + "\n" + \
            ">"
        return ret
