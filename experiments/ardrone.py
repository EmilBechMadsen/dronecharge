import time
import logging
import cv2
import freenect
from pid import PID
from libardrone.libardrone import ARDrone
from visual import centerFromImage, angleFromCenterAndTail


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


win = cv2.namedWindow("Win")

drone = ARDrone(True, True)

# logger.info("Battery Level: %s", drone.get_navdata()[0]['battery'])

try:
    is_flying = False

    x_pid = PID(Kp=1, Kd=0.8, Ki=0)
    y_pid = PID(Kp=1, Kd=0.8, Ki=0)

    angle_pid = PID(Kp=1, Kd=0.8, Ki=0)

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
        elif k == ord('r'):
            drone.reset()
            logger.info("Reset")
        elif k == ord('s') or k == ord('q'):
            break

        image = freenect.sync_get_video()[0]
        image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)

        image_center = (int(image.shape[1] / 2.0), int(image.shape[0] / 2.0))
        center = centerFromImage(image, 10, 20)
        tail = centerFromImage(image, 75, 85)

        cv2.line(image, image_center, tuple(center), (255, 0, 0))

        distance_x = center[0] - image_center[0]
        distance_y = center[1] - image_center[1]

        distance_x /= -320.0
        distance_y /= -240.0

        angle = angleFromCenterAndTail(center, tail) / -180.0

        rl = x_pid.GenOut(distance_x)
        fb = y_pid.GenOut(distance_y)
        aa = angle_pid.GenOut(angle)

        logger.info("RL: %s FB: %s AA: %s", rl, fb, aa)

        drone.at_cmd(True, rl, fb, 0, aa)

        bat = drone.get_navdata()[0]['battery']

        cv2.putText(image, "Bat: {}".format(bat), (20, 20), cv2.cv.CV_FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))

        cv2.imshow("Win", image)

except Exception, e:
    logger.warning("Exception %s", e)
finally:
    # drone.reset()
    drone.land()
    drone.halt()
    logger.info("Halt")