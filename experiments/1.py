import time
import cv2
import freenect
import numpy as np
from drone import Drone
from visual import droneCenterFromImage, droneTailCenterFromImage, angleFromCenterAndTail
from matplotlib.pylab import ion, legend, plot, draw


def add_line(text, offset):
    cv2.putText(
        image,
        text,
        (10, offset),
        cv2.FONT_HERSHEY_PLAIN,
        0.8,
        (0, 0, 255)
    )

window = cv2.namedWindow("win")
cv2.moveWindow("win", 800, 30)

drone = Drone()

ion()                           # interaction mode needs to be turned off

x = np.arange(0, 100, 1)         # we'll create an x-axis from 0 to 2 pi
yaw_error = np.arange(0, 100, 1, dtype="float")
yaw_line, = plot(x, x, label="Yaw")
yaw_line.axes.set_ylim(-350, 350)

roll_error = np.arange(0, 100, 1, dtype="float")
roll_line, = plot(x, x, label="Roll")
roll_line.axes.set_ylim(-350, 350)

pitch_error = np.arange(0, 100, 1, dtype="float")
pitch_line, = plot(x, x, label="Pitch")
pitch_line.axes.set_ylim(-350, 350)

legend()

starttime = time.time()         # this is our start time
t = 0                           # this is our relative start time
prevImageCenter = [0, 0]
prevTailCenter = [0, 0]
key = ''
while True:
    key = cv2.waitKey(1)

    if key == ord('q'):
        drone.disconnect()
        break

    if key == ord('r'):
        drone.reconnect()

    # thrust
    if key == 63232:
        drone.thrust += 1000
    elif key == 63233:
        drone.thrust -= 1000
    # emergency stop
    elif key == ord('s'):
        drone.stop()

    image = np.zeros((480, 640))
    image = freenect.sync_get_video()[0]
    image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)

    imageCenter = droneCenterFromImage(image)
    tailCenter = droneTailCenterFromImage(image)

    imageCenter[0] -= 320
    imageCenter[1] -= 240

    tailCenter[0] -= 320
    tailCenter[1] -= 240

    if imageCenter[0] == -320 and imageCenter[1] == -240:
        imageCenter = prevImageCenter
    else:
        prevImageCenter = imageCenter

    if tailCenter[0] == -320 and tailCenter[1] == -240:
        tailCenter = prevTailCenter
    else:
        prevTailCenter = tailCenter

    drone.angle = angleFromCenterAndTail(imageCenter, tailCenter)

    drone.update(
        roll_error=-imageCenter[0],
        pitch_error=imageCenter[1],
        yaw_error=-drone.angle
    )

    yaw_error = np.append(yaw_error, drone.angle)[1:]
    roll_error = np.append(roll_error, imageCenter[1])[1:]
    pitch_error = np.append(pitch_error, imageCenter[0])[1:]

    # update the plot data
    yaw_line.set_ydata(yaw_error)
    roll_line.set_ydata(roll_error)
    pitch_line.set_ydata(pitch_error)

    draw()

    add_line("Roll  : {0:.4} {1:.4}".format(
        drone.roll, drone.stabilizer_roll), 20)
    add_line("Pitch : {0:.4} {1:.4}".format(
        drone.pitch, drone.stabilizer_pitch), 40)
    add_line("Yaw   : {0:.4} {1:.4}".format(
        drone.yaw, drone.stabilizer_yaw), 60)
    add_line("Thrust: {0}".format(drone.thrust), 80)
    add_line("Bat   : {0}".format(drone.bat), 100)

    add_line("Angle : {0:.4}".format(drone.angle), 120)

    add_line("X     : {0}".format(imageCenter[0]), 140)
    add_line("Y     : {0}".format(imageCenter[1]), 160)

    # add_line("Error : {0}".format(yaw_pid.error), 160)

    # Draw Drone Position
    cv2.circle(
        image,
        (imageCenter[0] + 320, imageCenter[1] + 240),
        5,
        (0, 255, 255),
        -1
    )

    cv2.circle(
        image,
        (tailCenter[0] + 320, tailCenter[1] + 240),
        5,
        (255, 255, 0),
        -1
    )

    cv2.imshow("win", image)
