from dckit.tasks.task import Task
import time
import logging
import numpy as np


logger = logging.getLogger(__name__)


class VideoRecordTask(Task):
    def __init__(self, name):
        super(VideoRecordTask, self).__init__(name)

        self.isCompleted = False
        self.required_capabilities = [
            "videorecord"
        ]

    def start(self):
        if self.drone is None:
            logger.warn("VideoRecordTask started with no drone assigned!")
            return
        logger.debug("Started VideoRecordTask Task")
        self.drone.startRecording()
        self.isCompleted = True

    def isComplete(self):
        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<VideoRecordTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
