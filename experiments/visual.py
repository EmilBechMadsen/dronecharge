import cv2
import numpy as np


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


def droneCenterFromImage(image):
    return centerFromImage(image, 135, 150)


def droneTailCenterFromImage(image):
    return centerFromImage(image, 85, 100)


def centerFromImage(image, hue_min, hue_max):
    image = cv2.cvtColor(image, cv2.cv.CV_RGB2HSV)
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
