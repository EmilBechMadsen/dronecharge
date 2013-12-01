import numpy as np
import cv2
import freenect

cv2.namedWindow("Image")
cv2.moveWindow("Image", 0, 30)

cv2.namedWindow("Tresh")
cv2.moveWindow("Tresh", 800, 30)

cv2.namedWindow("Value")
cv2.moveWindow("Value", 800, 500)

cv2.namedWindow("Saturation")
cv2.moveWindow("Saturation", 0, 500)

x = 0
y = 0


def mouseCallback(event, _x, _y, flag, param):
    global x
    global y

    x = _x
    y = _y

cv2.cv.SetMouseCallback("Image", mouseCallback)

key = ''
while True:
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

    image = np.zeros((480, 640))

    orig = freenect.sync_get_video()[0]
    orig = cv2.cvtColor(orig, cv2.cv.CV_BGR2RGB)
    image = cv2.cvtColor(orig, cv2.cv.CV_RGB2HSV)
    hue = image[:, :, 0]
    value = image[:, :, 2]
    saturation = image[:, :, 1]

    cv2.circle(orig, (x, y), 3, (0, 0, 0), 1)

    print("x: {0} y: {1} hue: {2}".format(x, y, hue[y][x]))

    # orig[:,:,0] = 0
    # orig[:,:,1] = 0

    # 10-60 // green circle
    # 165-180 // blue circle

    hue[hue < 70] = 0
    hue[hue > 100] = 0
    hue[hue > 0] = 255

    hue = cv2.erode(hue, None, iterations=2)
    hue = cv2.dilate(hue, None, iterations=2)
    cv2.imshow("Tresh", hue)
    contours, hierarchy = cv2.findContours(
        hue,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) > 0:
        contour = contours[0]
        area = cv2.contourArea(contour)

        for c in contours:
            if cv2.contourArea(c) > area:
                area = cv2.contourArea(c)
                contour = c

        m = cv2.moments(contour)
        center = (0, 0)
        if m['m00'] != 0:
            center = (m['m10'] / m['m00'], m['m01'] / m['m00'])

        center = (int(center[0]), int(center[1]))

        # print('Center x:{} y:{}'.format(center[0], center[1]))

        cv2.circle(orig, center, 5, (255, 0, 255), -1)

    cv2.imshow("Image", orig)
    cv2.imshow("Value", value)
    cv2.imshow("Saturation", saturation)