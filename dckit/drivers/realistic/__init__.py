from dckit.drone import Drone
import time


class RealisticDrone(Drone):
    """docstring for RealisticDrone"""
    def __init__(self, name, environment=None):
        super(RealisticDrone, self).__init__(name, environment)
        self.battery_level = 1.0
        self.diameter = 0.0

        self.position = (0, 0, 0)
        self.target = (0, 0, 0)

        self.capabilities = [
            "move"
        ]

    def initialize(self):
        pass

    def move(self, position):
        self.target = position

        progress = 0.0
        original_position = self.position

        while progress < 1.0:
            self.position = (
                progress * self.target[0] + (1.0 - progress) * original_position[0],
                progress * self.target[1] + (1.0 - progress) * original_position[1],
                progress * self.target[2] + (1.0 - progress) * original_position[2]
            )

            time.sleep(0.5)
            progress += 0.05
            progress = min(progress, 1.0)

        self.position = self.target

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
