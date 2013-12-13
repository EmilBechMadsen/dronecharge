import time
import logging
from libardrone.libardrone import ARDrone


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


drone = ARDrone(True, True)

try:
    drone.reset()

    drone.takeoff()

    logger.info("Takeoff")

    time.sleep(5)

    drone.hover()
    logger.info("Hover")

    time.sleep(1)

    drone.land()
    logger.info("Land")
finally:
    # drone.reset()
    drone.halt()
    logger.info("Halt")