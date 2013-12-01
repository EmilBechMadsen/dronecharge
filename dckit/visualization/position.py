import cv2
import numpy as np
import time
import logging
import random
import freenect
logger = logging.getLogger(__name__)


class PositionVisualizer(object):
    """docstring for PositionVisualizer"""
    def __init__(self, drones):
        super(PositionVisualizer, self).__init__()

        self.drones = drones

        self.init()

    def init(self):
        self.win = "Position"
        self.have_kinect = False
        self.img = None

        video = freenect.sync_get_video()
        if video is not None:
            self.have_kinect = True

        cv2.startWindowThread()
        cv2.namedWindow(self.win)
        cv2.moveWindow(self.win, 800, 0)
        cv2.resizeWindow(self.win, 500, 500)

    def visualize(self):
        size = (640, 480)
        drone_size = 3
        charger_size = 6

        if self.have_kinect:
            img, _ = freenect.sync_get_video()
            img = cv2.cvtColor(img, cv2.cv.CV_BGR2RGB)
        else:
            if self.img is None:
                self.img = np.zeros((size[1], size[0], 3))
            img = self.img
            img[:, :, :] = 0

        colors = [
            (0, 0, 255),
            (0, 255, 0),
            (255, 0, 0),
            (255, 255, 0),
            (255, 0, 255)
        ]

        for i, drone in enumerate(self.drones):
            charger_top_left = (
                int(drone.charger.coordinates[0] - charger_size / 2 + size[0] / 2),
                int(drone.charger.coordinates[1] - charger_size / 2 + size[1] / 2)
            )

            charger_bottom_right = (
                int(drone.charger.coordinates[0] + charger_size / 2 + size[0] / 2),
                int(drone.charger.coordinates[1] + charger_size / 2 + size[1] / 2)
            )

            cv2.rectangle(img, charger_top_left, charger_bottom_right, colors[i], 1)
            position = (
                int(drone.position[0] + size[0] / 2),
                int(drone.position[1] + size[1] / 2)
            )

            # drone's path
            beginning = (
                int(drone.position[0] + size[0] / 2),
                int(drone.position[1] + size[1] / 2)
            )

            end = (
                int(drone.target[0] + size[0] / 2),
                int(drone.target[1] + size[1] / 2)
            )
            cv2.line(img, beginning, end, colors[i], 1)

            # bounding box
            cv2.circle(img, position, int(drone.bounding_radius), (100, 100, 100), 1)

            # drone
            cv2.circle(img, position, drone_size, colors[i], -1)

            # battery level
            cv2.putText(img, "%s Battery: %s%%" % (drone.name, drone.battery_level * 100), (10, 20 * i + 20), cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))

            #logger.info("Position: %s", position)

        cv2.imshow(self.win, img)
        cv2.waitKey(1)
        del img

