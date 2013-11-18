from dckit.drone import Drone


class IdealDrone(Drone):
    """docstring for Crazyflie"""
    def __init__(self, name, environment=None):
        super(IdealDrone, self).__init__(name, environment)
        self.battery_level = 1.0
        self.diameter = 0.0
        self.actualHeadin = 0.0
        self.targetHeading = 0.0

        self.actualPosition = (0, 0, 0)
        self.targetPosition = (0, 0, 0)

        self.capabilities = [
            "move"
        ]

    def initialize(self):
        pass

    def setHeading(self, heading):
        assert heading >= 0.0 and heading < 360.0
        self.targetHeading = heading
        self.actualHeading = heading  # Instant turning
        # Actually change the drones heading (Not needed in simulation)

    def getHeading(self):
        return self.actualHeading

    def move(self, position):
        self.targetPosition = position
        self.actualPosition = position  # Instant movement.
        # Start moving (Not needed in instant-simulation)

    def noop(self):
        # hover in place
        pass

    def getBatteryLevel(self):
        # return battery level normalized to 0.0 - 1.0
        return self.battery_level

    def getPosition(self):
        # return drone's position in the environment's coordinate system
        return self.actualPosition

    def getDroneDiameter(self):
        # return drone size in the environment's coordinate system
        return self.diameter

    def isCharged(self):
        return self.battery_level > 0.8
