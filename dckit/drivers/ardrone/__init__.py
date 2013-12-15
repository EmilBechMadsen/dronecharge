from dckit.drone import Drone
from dckit.drivers.ardrone.libardrone import ARDrone as ARDroneAPI
from dckit.drivers.ardrone.visual import centerFromImage, angleFromCenterAndTail
from dckit.drivers.ardrone.pid import PID
import time
import logging
import freenect
import cv2
import numpy as np


logger = logging.getLogger(__name__)


class ARDrone(Drone):
    """docstring for KinectDrone"""
    def __init__(self, name, environment=None):
        super(ARDrone, self).__init__(name, environment)
        self.battery_level = 1.0
        self.diameter = 0.0

        self.original_position = np.array([0, 0, 0])
        self.position = np.array([0, 0, 0])
        self.target = np.array([0, 0, 0])

        self.capabilities = [
            "move"
        ]

        self.is_flying = False
        self.low_battery_level = 0.1

        video = freenect.sync_get_video()
        self.have_kinect = video is not None

        self.drone = ARDroneAPI(True, True)

    def initialize(self):
        self.target = self.position

    def isBatteryLow(self): ## DRAINS 0.8 OF BATTERY PER TASK (Intended to run out fast for testing)
        self.battery_level = self.battery_level - 0.1 if ((self.battery_level - 0.1) >= 0.0) else self.low_battery_level * 2.0
        logger.info("%s - %s", self.name, self.battery_level)
        return self.low_battery_level * 2.0 >= self.battery_level

    def move(self, position):
        self.target = position
        self.original_position = self.position

    def noop(self):
        # hover in place
        pass

    def getBatteryLevel(self):
        return self.battery_level

    def getPosition(self):
        # return drone's position in the environment's coordinate system
        return self.position

    def getDroneDiameter(self):
        # return drone size in the environment's coordinate system
        return self.diameter

    def isCharged(self):
        return self.battery_level > 0.8

    def setState(self, state):
        pass

    def takeoff(self):
        logger.info("Drone takeoff")
        self.drone.takeoff()
        time.sleep(5)
        self.is_flying = True

    def land(self):
        logger.info("Drone land")
        self.drone.land()
        self.is_flying = False

    def hover(self):
        self.drone.hover()

    def controlLoop(self):
        try:
            kp = 0.2
            kd = 0.1
            ki = 0.0005

            x_pid = PID(Kp=kp, Kd=kd, Ki=ki)
            y_pid = PID(Kp=kp, Kd=kd, Ki=ki)

            angle_pid = PID(Kp=1.5, Kd=0.5, Ki=0.05)

            while True:
                image = freenect.sync_get_video()[0]
                image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)

                target = (int(self.target[0] + 320), int(self.target[1] + 240))
                center = centerFromImage(image, 10, 20)
                tail = centerFromImage(image, 75, 90)

                cv2.line(image, target, tuple(center), (255, 0, 0))
                cv2.circle(image, tuple(center), 3, (0, 0, 255), -1)
                cv2.circle(image, tuple(tail), 3, (255, 0, 0), -1)
                cv2.circle(image, target, 10, (0, 0, 0), 3)

                distance_x = center[0] - target[0]
                distance_y = center[1] - target[1]

                distance_x /= -320.0
                distance_y /= -240.0

                angle = angleFromCenterAndTail(center, tail) / -180.0

                rl = x_pid.GenOut(distance_x)
                fb = y_pid.GenOut(distance_y)
                aa = angle_pid.GenOut(angle)

                if np.isnan(aa):
                    aa = 0.0

                self.position = (center[0] - 320.0, center[1] - 240.0, 10)

                if self.isAtTarget(self.charger.getCoordinates(), 20) and self.battery_level < 1.0: # If at charger, slowly charge
                    self.battery_level += 0.01

                if self.is_flying:
                    self.drone.at_cmd(True, rl, fb, 0, aa)
                    # logger.info("Set Drone: %s, %s, %s", rl, fb, aa)
        except Exception, e:
            logger.warning("Exception %s", e)
        finally:
            # drone.reset()
            self.drone.land()
            self.drone.halt()
            logger.info("Drone Stopped")
