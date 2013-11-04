from dckit import Enum


class TaskState(Enum):
    READY = 0
    EXECUTING = 1
    COMPLETE = 2


class Task(object):
    """Top level task class for defining "jobs" for the drones
    """

    drone = None
    subtasks = []
    state = TaskState.READY
    capabilities = []

    def __init__(self, arg):
        super(Task, self).__init__()
        self.arg = arg

    def start(self):
        self.state = TaskState.EXECUTING

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

            if currentSubtask is None:
                continue

            ready = currentSubtask.state == TaskState.READY
            executing = currentSubtask.state == TaskState.EXECUTING

            if ready or executing:
                return currentSubtask

        return TaskState.COMPLETE

    def isComplete(self):
        pass

    def setCapabilities(self, capabilities):
        self.capabilities = capabilities
