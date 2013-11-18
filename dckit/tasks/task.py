from dckit.enum import Enum
from threading import Thread
import logging


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
        self.parent = None
        self.subtasks = []
        self.state = TaskState.READY
        self.required_capabilities = []
        self.environment = environment
        self.ignores_low_battery = False

    def start(self):
        self.state = TaskState.EXECUTING

    def isComplete(self):
        pass

    def setDrone(self, drone):
        for subTask in self.subtasks:
            subTask.setDrone(drone)
        self.drone = drone

    def setCapabilities(self, capabilities):
        self.required_capabilities = capabilities

    def addSubtask(self, task):
        task.parent = self
        self.subtasks.append(task)

    def accumulateCapabilities(self):
        logger.debug("Accumulating subtask capabilities")

        if len(self.subtasks) == 0:
            return set(self.required_capabilities)

        self.required_capabilities = set(self.required_capabilities)

        for subtask in self.subtasks:
            caps = subtask.accumulateCapabilities()
            self.required_capabilities = self.required_capabilities.union(caps)

        return self.required_capabilities

    def evaluate(self):
        logger.debug("Evaluating task: %s", self)
        currentSubtask = self.getCurrentSubtask()
        if currentSubtask is None:
            if self.isComplete():
                self.state = TaskState.COMPLETE
                logger.debug("Task Complete %s", self)

            return

        # currentSubtask can be the state directly
        # when its entire subtree is complete
        if currentSubtask == TaskState.COMPLETE:
            self.state = TaskState.COMPLETE
            logger.debug("Task Subtree Complete %s", self)
            return

        if currentSubtask.state == TaskState.READY:
            if not self.ignores_low_battery:
                drone = self.environment.replaceDroneIfNeeded(
                    self.drone,
                    self.required_capabilities
                )

            if drone is None:
                logger.info(
                    "No drone available to perform the task. " +
                    "Required capabilities: %s", self.required_capabilities
                )
                return

            if self.drone is not None and self.drone != drone:
                original_state = self.drone.getState()

                from dckit.tasks.replacement_task import ReplacementTask

                replacement_task = ReplacementTask()
                replacement_task.originalState = original_state

                replacement_task.setDrone(drone)

                # Insert replacement taks before current subtask
                parent = currentSubtask.parent
                currentSubtaskIndex = parent.subtasks.index(currentSubtask)
                parent.subtasks = \
                    parent.subtasks[:currentSubtaskIndex] +\
                    [replacement_task] + \
                    parent.subtasks[currentSubtaskIndex:]

                logger.debug("Sent drone to charge %s", self.drone)

                self.setDrone(drone)

                logger.debug("New drone is %s", self.drone)

                return

            self.setDrone(drone)
            currentSubtask.setDrone(drone)

            self.state = TaskState.EXECUTING
            currentSubtask.state = TaskState.EXECUTING
            Thread(name=None, target=currentSubtask.start).start()
            logger.debug("Started task %s", currentSubtask)
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

        # Non-leaf tasks must be of type Task
        if type(self).__name__ != Task.__name__:
            logger.warning(
                "Only leaf nodes are executed, %s is not a leaf node, will not be executed",
                self.__class__.__name__
            )

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
