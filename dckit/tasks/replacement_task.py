from dckit.tasks.task import Task
import time
import logging


logger = logging.getLogger(__name__)


class ReplacementTask(Task):
    def __init__(self, name, targetPosition):
        super(ReplacementTask, self).__init__(name)

        self.originalState = {}
        self.isCompleted = False
        self.targetPosition = targetPosition
        self.required_capabilities = [
            "move"
        ]

    def start(self):
        if self.drone is None:
            logger.warn("ReplacementTask started with no drone assigned!")
            return

        #time.sleep(0.01)

        self.drone.move(self.targetPosition)
        if self.drone.actualPosition == self.drone.targetPosition:
            self.isCompleted = True

    def isComplete(self):
        if self.isCompleted:
            self.drone.setState(self.originalState)

        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<ReplacementTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
