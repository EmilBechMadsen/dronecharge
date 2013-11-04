from dckit.environment import Environment
from dckit.tasks.task import TaskState


class DCKit(object):
    """Main class that encapsulates everything

    """

    environment = None
    tasks = []
    drones = []

    def __init__(self):
        super(DCKit, self).__init__()

        self.environment = Environment()

    def addDrone(self, drone):
        self.drones.append(drone)

    def addTask(self, task):
        self.tasks.append(task)

    def _main_loop(self):
        while True:
            # self.environment
            for task in self.tasks:
                task.evaluate()
                if task.state == TaskState.COMPLETE:
                    break

        print("DONE")
