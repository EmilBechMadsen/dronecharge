import time
import logging
import cv2
import freenect
import math
from pid import PID
from libardrone.libardrone import ARDrone
from visual import centerFromImage, angleFromCenterAndTail


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


target_x = 320.0
target_y = 240.0

def mouseCallback(event, _x, _y, flag, param):
    global target_x
    global target_y

    if event != 4:
        return

    logger.info("Event: %s Flag: %s", event, flag)

    target_x = _x
    target_y = _y

win = cv2.namedWindow("Win")
cv2.setMouseCallback("Win", mouseCallback)

drone = ARDrone(True, True)

# logger.info("Battery Level: %s", drone.get_navdata()[0]['battery'])

try:
    is_flying = False

    kp = 0.2
    kd = 0.1
    ki = 0.0005

    x_pid = PID(Kp=kp, Kd=kd, Ki=ki)
    y_pid = PID(Kp=kp, Kd=kd, Ki=ki)

    angle_pid = PID(Kp=1.5, Kd=0.5, Ki=0.05)

    while True:
        k = cv2.waitKey(1)

        if k == ord(' ') and not is_flying:
            drone.takeoff()
            logger.info("Takeoff")
            is_flying = not is_flying
        elif k == ord(' ') and is_flying:
            drone.land()
            logger.info("Landing")
            is_flying = not is_flying
        elif k == ord('d') and is_flying:
            drone.event_boom()
            logger.info("Dance")
            time.sleep(3)
        elif k == ord('r'):
            drone.reset()
            logger.info("Reset")
        elif k == ord('s') or k == ord('q'):
            break

        image = freenect.sync_get_video()[0]
        image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)

        image_center = (int(image.shape[1] / 2.0), int(image.shape[0] / 2.0))
        target = (int(target_x), int(target_y))
        center = centerFromImage(image, 10, 20)
        tail = centerFromImage(image, 75, 90)

        cv2.line(image, target, tuple(center), (255, 0, 0))
        cv2.circle(image, tuple(center), 3, (0, 0, 255), -1)
        cv2.circle(image, tuple(tail), 3, (255, 0, 0), -1)
        cv2.circle(image, (int(target_x), int(target_y)), 10, (0, 0, 0), 3)

        distance_x = center[0] - target[0]
        distance_y = center[1] - target[1]

        distance_x /= -320.0
        distance_y /= -240.0

        angle = angleFromCenterAndTail(center, tail) / -180.0

        # logger.info("Correcting angle: %s", angle)
        # if abs(angle) > 0.05:
        #     # logger.info("Correcting angle: %s", angle)
        #     distance_x = 0.0
        #     distance_y = 0.0

        rl = x_pid.GenOut(distance_x)
        fb = y_pid.GenOut(distance_y)
        aa = angle_pid.GenOut(angle)

        if math.isnan(aa):
            aa = 0.0

        drone.at_cmd(True, rl, fb, 0, aa)

        navdata = drone.get_navdata()
        bat = navdata[0]['battery']

        # logger.info("RL: %s FB: %s AA: %s BAT: %s", rl, fb, aa, bat)
        # logger.info(navdata)
        cv2.putText(image, "Bat: {}".format(bat), (20, 20), cv2.cv.CV_FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

        cv2.imshow("Win", image)

except Exception, e:
    logger.warning("Exception %s", e)
finally:
    # drone.reset()
    drone.land()
    drone.halt()
    logger.info("Halt")