from dckit.environment import Environment
from dckit.tasks.task import TaskState


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

    def _main_loop(self):
        i = 0
        while True:
            # self.environment
            for task in self.tasks:
                if task.environment is None:
                    task.environment = self.environment

                if task.state == TaskState.COMPLETE:
                    task.evaluate()
                    print("DONE")
                    return
                task.evaluate()
                print("\nIteration: " + str(i))
                print(task)

            i += 1
