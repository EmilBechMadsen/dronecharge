from dckit.environment import Environment
from dckit.tasks.task import TaskState
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DCKit(object):
    """Main class that encapsulates everything

    """

    def __init__(self):
        super(DCKit, self).__init__()

        self.environment = Environment()
        self.tasks = []

    def addDrone(self, drone):
        drone.environment = self.environment
        self.environment.addDrone(drone)

    def addTask(self, task):
        self.tasks.append(task)

    def _accumulateCapabilities(self):
        for task in self.tasks:
            task.accumulateCapabilities()

    def _iterate(self, iteration):
        for task in self.tasks:
            if task.environment is None:
                task.environment = self.environment

            if task.state == TaskState.COMPLETE:
                task.evaluate()
                logger.info("DONE")
                return False

            task.evaluate()
            logger.debug("\nIteration: " + str(iteration))
            logger.debug(task)

    def _main_loop(self):
        self._accumulateCapabilities()

        i = 0
        while True:
            # self.environment
            if not self._iterate(i):
                return
            i += 1
