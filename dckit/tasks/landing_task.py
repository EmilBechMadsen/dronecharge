from dckit.tasks.task import Task, TaskState
import logging
logger = logging.getLogger(__name__)

class LandingTask(Task):
    def __init__(self, name, targetPosition):
        super(LandingTask, self).__init__(name)

        self.isCompleted = False
        self.targetPosition = targetPosition
        self.required_capabilities = [
            "move"
        ]

    def start(self):
        self.state = TaskState.EXECUTING
        self.drone.move(self.targetPosition)

    def isComplete(self):
        if self.drone.position == self.drone.target:
            self.isCompleted = True
        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<LandingTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
