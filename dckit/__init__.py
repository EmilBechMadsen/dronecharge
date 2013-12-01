from dckit.environment import Environment
from dckit.tasks.task import TaskState
from threading import Thread
import logging
import time
import sys


logger = logging.getLogger(__name__)


class DCKit(object):
    """Main class that encapsulates everything

    """

    def __init__(self):
        super(DCKit, self).__init__()

        self.environment = Environment()

    def addDrone(self, drone):
        drone.environment = self.environment
        self.environment.addDrone(drone)

    def addTask(self, task):
        self.environment.addTask(task)

    def run(self, visualize=False):
        self._main_loop(visualize)

    def _accumulateCapabilities(self):
        tasks = self.environment.tasks
        for task in tasks:
            task.accumulateCapabilities()

    def _iterate(self, iteration):
        tasks = self.environment.tasks

        for task in tasks:
            if task.environment is None:
                task.environment = self.environment

            if task.state == TaskState.COMPLETE:
                task.evaluate()
                logger.info("DONE")
                return False

            task.evaluate()

            logger.debug("\nIteration: " + str(iteration))
            #logger.debug(task)

        return True

    def _main_loop(self, visualize=False):
        if visualize:
            logger.info("Running with visualizations")
            from dckit.visualization.task_tree import TaskVisualizer
            from dckit.visualization.position import PositionVisualizer

            task_visualizer = TaskVisualizer(self.environment.tasks)
            position_visualizer = PositionVisualizer(self.environment.getAllDrones())
            logger.info(self.environment.getAllDrones())

        self._accumulateCapabilities()

        if visualize:
            pass
            #Thread(name=None, target=position_visualizer.visualize).start()
            #Thread(name=None, target=task_visualizer.visualize).start()

        i = 0
        while True:
            logger.info("Iteration %s", i)
            # self.environment

            if not self._iterate(i):
                logger.debug("Iterate finished last iteration")
                return

            if visualize:
                task_visualizer.visualize()
                position_visualizer.visualize()

            i += 1
