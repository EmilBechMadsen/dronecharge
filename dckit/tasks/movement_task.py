from dckit.tasks.task import Task
import time
import logging
import numpy as np


logger = logging.getLogger(__name__)


class MovementTask(Task):
    def __init__(self, name, targetPosition):
        super(MovementTask, self).__init__(name)

        self.isCompleted = False
        self.target = targetPosition
        self.required_capabilities = [
            "move"
        ]

    def start(self):
        if self.drone is None:
            logger.warn("MovementTask started with no drone assigned!")
            return

        logger.debug("Started Movement Task")
        self.drone.move(self.target)

        while True:
            if self.drone.isAtTarget(self.target):
                self.isCompleted = True
                logger.debug("Stopped Movement Task")
                break

            time.sleep(0.05)

    def isComplete(self):
        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<MovementTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
