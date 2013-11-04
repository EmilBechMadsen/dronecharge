from dckit.drone import Drone


class Crazyflie(Drone):
    """docstring for Crazyflie"""
    def __init__(self):
        super(Crazyflie, self).__init__()

    def initialize(self):
        pass

    def setHeading(self, heading):
        assert heading >= 0.0 and heading < 360.0
        # do something

    def getHeading(self):
        return 360.0

    def setForwardSpeed(self, speed):
        # speed is normalized to 0.0 - 1.0
        pass

    def setClimbRate(self, climb_rate):
        # climb_rate is normalized to 0.0 - 1.0
        pass

    def noop(self):
        # hover in place
        pass

    def getBatteryLevel(self):
        # return battery level normalized to 0.0 - 1.0
        self.battery = 10

    def getPosition(self):
        # return drone's position in the environment's coordinate system
        raise NotImplementedError("Please Implement this method")

    def getDroneDiameter(self):
        # return drone size in the environment's coordinate system
        pass
