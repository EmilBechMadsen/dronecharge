from dckit.tasks.task import Task, TaskState
import numpy as np
import logging
import time
logger = logging.getLogger(__name__)

class TakeoffTask(Task):
    def __init__(self, name="Takeoff"):
        super(TakeoffTask, self).__init__(name)

        self.isCompleted = False
        self.target = (0, 0, 0)
        self.required_capabilities = [
            "move"
        ]

    def start(self):
        logger.info("Task Takeoff Start")
        self.state = TaskState.EXECUTING
        self.target = self.drone.position
        self.drone.takeoff()
        time.sleep(3)
        self.isCompleted = True

    def isComplete(self):
        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<LandingTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
