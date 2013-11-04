from dckit.drone import Drone


class Ideal(Drone):
    battery = 1
    diameter = 10.0
    actualHeading = 0.0
    targetHeading = 0.0

    actualPosition = (0, 0, 0)
    targetPosition = (0, 0, 0)

    """docstring for Crazyflie"""
    def __init__(self, name, environment):
        super(Ideal, self).__init__(name, environment)

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
        return self.battery

    def getPosition(self):
        # return drone's position in the environment's coordinate system
        return self.actualPosition

    def getDroneDiameter(self):
        # return drone size in the environment's coordinate system
        return self.diameter
