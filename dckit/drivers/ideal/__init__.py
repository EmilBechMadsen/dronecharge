from dckit.drone import Drone


class IdealDrone(Drone):
    """docstring for Crazyflie"""
    def __init__(self, name, environment=None):
        super(IdealDrone, self).__init__(name, environment)
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
        self.position = position  # Instant movement.
        # Start moving (Not needed in instant-simulation)

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
