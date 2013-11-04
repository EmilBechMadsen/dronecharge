from dckit.enum import Enum


class TaskState(Enum):
    READY = 0
    EXECUTING = 1
    COMPLETE = 2


class Task(object):
    """Top level task class for defining "jobs" for the drones
    """

    def __init__(self, name="Task"):
        super(Task, self).__init__()

        self.name = name
        self.drone = None
        self.subtasks = []
        self.state = TaskState.READY
        self.capabilities = []

    def start(self):
        self.state = TaskState.EXECUTING

    def isComplete(self):
        pass

    def setCapabilities(self, capabilities):
        self.capabilities = capabilities

    def addSubtask(self, task):
        self.subtasks.append(task)

    def evaluate(self):
        currentSubtask = self.getCurrentSubtask()

        if currentSubtask is None:
            if self.isComplete():
                self.state = TaskState.COMPLETE

            return

        # currentSubtask can be the state directly, remember?
        if currentSubtask == TaskState.COMPLETE:
            self.state = TaskState.COMPLETE
            return

        if currentSubtask.state == TaskState.READY:
            self.state = TaskState.EXECUTING
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

            if currentSubtask is None or currentSubtask == TaskState.COMPLETE:
                continue

            ready = currentSubtask.state == TaskState.READY
            executing = currentSubtask.state == TaskState.EXECUTING

            if ready or executing:
                return currentSubtask

        return TaskState.COMPLETE

    def __repr__(self):
        ret = "<Task (" + str(id(self)) + "): \n" + \
            "    Drone: " + str(self.drone) + " \n" + \
            "    Subtasks: " + str(self.subtasks) + " \n" + \
            "    State: " + str(self.state) + " \n" + \
            "    Capabilities: " + str(self.capabilities) + "\n" + \
            ">"
        return ret
