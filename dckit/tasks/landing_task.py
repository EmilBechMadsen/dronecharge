from dckit.tasks.task import Task, TaskState
import numpy as np
import logging
import time
logger = logging.getLogger(__name__)

class LandingTask(Task):
    def __init__(self, name="Landing", target=(0, 0, 0)):
        super(LandingTask, self).__init__(name)

        self.isCompleted = False
        self.target = target
        self.required_capabilities = [
            "move"
        ]

    def start(self):
        self.state = TaskState.EXECUTING
        time.sleep(5)
        self.drone.land()

    def isComplete(self):
        return True

    def __repr__(self):
        ret = "\n\t<LandingTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
