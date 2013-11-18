from dckit.tasks.task import Task
import time
import logging


logger = logging.getLogger(__name__)


class MovementTask(Task):
    def __init__(self, name, targetPosition):
        super(MovementTask, self).__init__(name)

        self.isCompleted = False
        self.targetPosition = targetPosition
        self.required_capabilities = [
            "move"
        ]

    def start(self):
        if self.drone is None:
            logger.warn("MovementTask started with no drone assigned!")
            return

        time.sleep(1.0)

        self.drone.move(self.targetPosition)
        if self.drone.actualPosition == self.drone.targetPosition:
            self.isCompleted = True

    def isComplete(self):
        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<MovementTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
