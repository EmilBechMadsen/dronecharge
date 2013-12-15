import logging
from libardrone.libardrone import ARDrone


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


drone = ARDrone(True, True)

drone.land()
drone.halt()
logger.info("Halt")