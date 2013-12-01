from dckit.drone import Drone
import time
import logging
import numpy as np


logger = logging.getLogger(__name__)


class RealisticDrone(Drone):
    """docstring for RealisticDrone"""
    def __init__(self, name, environment=None):
        super(RealisticDrone, self).__init__(name, environment)
        self.battery_level = 1.0
        self.original_position = np.array([0, 0, 0])
        self.position = np.array([0, 0, 0])
        self.target = np.array([0, 0, 0])
        self.low_battery_level = 0.2

        self.capabilities = [
            "move",
            "videorecord"
        ]

        self.state["recordingVideo"] = False

    def initialize(self):
        pass

    def isBatteryLow(self): ## DRAINS 0.5 OF BATTERY PER TASK (Intended to run out fast for testing)
        self.battery_level = self.battery_level - 0.2 if ((self.battery_level - 0.2) >= 0.0) else self.low_battery_level * 2.0
        logger.info("%s - %s", self.name, self.battery_level)
        return self.low_battery_level * 2.0 >= self.battery_level

    def move(self, position):
        self.target = position
        self.original_position = self.position

    def noop(self):
        # hover in place
        pass

    def setState(self, state):
        if "recordingVideo" in state.keys():
            if state["recordingVideo"] is True and self.state["recordingVideo"] is False:
                self.startRecording()
            elif state["recordingVideo"] is False and self.state["recordingVideo"] is True:
                self.stopRecording()

    def getBatteryLevel(self):
        # return battery level normalized to 0.0 - 1.0
        return self.battery_level

    def getPosition(self):
        # return drone's position in the environment's coordinate system
        return self.position

    def isCharged(self):
        return self.battery_level > 0.8

    def controlLoop(self):
        while True:
            original = np.array(self.original_position, dtype=np.float32)
            position = np.array(self.position, dtype=np.float32)
            target = np.array(self.target, dtype=np.float32)

            diff = target - original

            if not self.isAtTarget(target, 1):
                position += (diff / 100.0)
                self.position = tuple(position)

            if self.isAtTarget(self.charger.getCoordinates()): # If at charger, slowly charge
                self.battery_level += 0.001

            time.sleep(0.05)

    def startRecording(self): # "Fake" method to simulate recording.
        self.state["recordingVideo"] = True

    def stopRecording(self): # "Fake" method to simulate stopping recording.
        self.state["recordingVideo"] = False