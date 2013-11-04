from dckit.environment import Environment
from dckit.task import Task, TaskState


class DCKit(object):
    """Main class that encapsulates everything

    """

    environment = None
    tasks = None
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


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
