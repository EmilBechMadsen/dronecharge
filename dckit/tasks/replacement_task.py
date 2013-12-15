from dckit.tasks.task import Task
import time
import logging
import numpy as np


logger = logging.getLogger(__name__)


class ReplacementTask(Task):
    def __init__(self, name, targetPosition, droneState):
        super(ReplacementTask, self).__init__(name)

        self.originalState = {}
        self.isCompleted = False
        self.targetPosition = targetPosition
        self.droneState = droneState
        self.required_capabilities = [
            "move"
        ]

    def start(self):
        if self.drone is None:
            logger.warn("ReplacementTask started with no drone assigned!")
            return

        self.drone.takeoff()
        self.drone.move(self.targetPosition)
        self.drone.setState(self.droneState)

    def isComplete(self):
        if self.drone.isAtTarget(self.targetPosition):
            self.isCompleted = True

        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<ReplacementTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
