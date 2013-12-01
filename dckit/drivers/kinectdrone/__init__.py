from dckit.drone import Drone
import time
import logging
import freenect
import cv2
import numpy as np


logger = logging.getLogger(__name__)


class KinectDrone(Drone):
    """docstring for KinectDrone"""
    def __init__(self, name, environment=None):
        super(KinectDrone, self).__init__(name, environment)
        self.battery_level = 1.0
        self.diameter = 0.0

        self.original_position = np.array([0, 0, 0])
        self.position = np.array([0, 0, 0])
        self.target = np.array([0, 0, 0])

        self.capabilities = [
            "move"
        ]

        self.hue_range = (75, 90)

        video = freenect.sync_get_video()
        self.have_kinect = video is not None

    def initialize(self):
        pass

    def isBatteryLow(self): ## DRAINS 0.8 OF BATTERY PER TASK (Intended to run out fast for testing)
        self.battery_level = self.battery_level - 0.3 if ((self.battery_level - 0.3) >= 0.0) else self.low_battery_level * 2.0
        return self.low_battery_level * 2.0 >= self.battery_level

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

    def setState(self, state):
        pass

    def controlLoop(self):
        while True:
            if self.loop_should_stop:
                break

            img, _ = freenect.sync_get_video()

            center = self.droneCenterFromImage(img)

            center = (
                int(center[0] - img.shape[1] / 2),
                int(center[1] - img.shape[0] / 2),
                1
            )

            del img

            logger.debug("Position: %s", center)

            self.position = center

            if self.isAtTarget(self.charger.getCoordinates(), 10): # If at charger, slowly charge
                self.battery_level += 0.005

    def angleFromCenterAndTail(center, tail):
        tail = np.array(tail)
        center = np.array(center)

        sign = np.sign(center[0] - tail[0])

        vec = np.array(tail - center, dtype='float32')
        vlen = np.linalg.norm(vec)
        vec[0] /= vlen
        vec[1] /= vlen

        angle = np.arccos(np.dot(vec, np.array([0, 1]))) * 180.0 / np.pi

        return sign * angle


    def droneCenterFromImage(self, image):
        return self.centerFromImage(image, self.hue_range[0], self.hue_range[1])


    def droneTailCenterFromImage(self, image):
        return self.centerFromImage(image, 85, 100)


    def centerFromImage(self, image, hue_min, hue_max):

        image = cv2.cvtColor(image, cv2.cv.CV_BGR2HSV)
        hue = image[:, :, 0]

        # Filter out green postit note color
        # yellow is 90-100
        # pink is 137-150
        # green is 80-90
        hue[hue < hue_min] = 0
        hue[hue > hue_max] = 0
        hue[hue > 0] = 255

        hue = cv2.erode(hue, None, iterations=2)
        hue = cv2.dilate(hue, None, iterations=2)

        contours, hierarchy = cv2.findContours(
            hue,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )

        center = [0, 0]

        if len(contours) > 0:
            contour = contours[0]
            area = cv2.contourArea(contour)

            for c in contours:
                if cv2.contourArea(c) > area:
                    area = cv2.contourArea(c)
                    contour = c

            m = cv2.moments(contour)
            center = [0, 0]
            if m['m00'] != 0:
                center = [m['m10'] / m['m00'], m['m01'] / m['m00']]

            center = [int(center[0]), int(center[1])]

        return center