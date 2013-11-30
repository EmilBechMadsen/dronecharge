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
        self.diameter = 0.0

        self.original_position = np.array([0, 0, 0])
        self.position = np.array([0, 0, 0])
        self.target = np.array([0, 0, 0])

        self.capabilities = [
            "move"
        ]

    def initialize(self):
        pass

    def move(self, position):
        self.target = position
        self.original_position = self.position

    def noop(self):
        # hover in place
        pass

    def getBatteryLevel(self):
        # return battery level normalized to 0.0 - 1.0
        return self.battery_level

    def getPosition(self):
        # return drone's position in the environment's coordinate system
        return self.position

    def getDroneDiameter(self):
        # return drone size in the environment's coordinate system
        return self.diameter

    def isCharged(self):
        return self.battery_level > 0.8

    def controlLoop(self):
        while True:
            original = np.array(self.original_position, dtype=np.float32)
            position = np.array(self.position, dtype=np.float32)
            target = np.array(self.target, dtype=np.float32)

            diff = target - original

            if not np.allclose(position, target):
                position += (diff / 100.0)
                self.position = tuple(position)

            time.sleep(0.05)