import cv2
import numpy as np
import time
import logging
import random


logger = logging.getLogger(__name__)


class PositionVisualizer(object):
    """docstring for PositionVisualizer"""
    def __init__(self, drones):
        super(PositionVisualizer, self).__init__()

        self.drones = drones

        self.init()

    def init(self):
        self.win = "Position"

        cv2.startWindowThread()
        cv2.namedWindow(self.win)
        cv2.moveWindow(self.win, 0, 0)
        cv2.resizeWindow(self.win, 500, 500)

    def visualize(self):
        size = 500
        drone_size = 3
        img = np.zeros((size, size, 3), dtype=np.uint8)

        #while True:
        img[:, :, :] = 0

        colors = [
            (0, 0, 255),
            (0, 255, 0),
            (255, 0, 0),
            (255, 255, 0),
            (255, 0, 255)
        ]

        for i, drone in enumerate(self.drones):
            position = (
                int(drone.position[0] + size / 2),
                int(drone.position[1] + size / 2)
            )

            # drone's path
            beginning = (
                int(drone.original_position[0] + size / 2),
                int(drone.original_position[1] + size / 2)
            )

            end = (
                int(drone.target[0] + size / 2),
                int(drone.target[1] + size / 2)
            )
            cv2.line(img, beginning, end, (100, 100, 100), 1)

            # bounding box
            cv2.circle(img, position, int(drone.bounding_radius), (100, 100, 100), 1)

            # drone
            cv2.circle(img, position, drone_size, colors[i], -1)

            #logger.info("Position: %s", position)

        cv2.imshow(self.win, img)
        cv2.waitKey(1)

