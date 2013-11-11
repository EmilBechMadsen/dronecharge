from dckit.tasks.task import Task
from dckit.tasks.task_state import TaskState


class MovementTask(Task):
    def __init__(self, name, targetPosition):
        super(MovementTask, self).__init__(name)

        self.isCompleted = False
        self.targetPosition = targetPosition

    def start(self):
        self.state = TaskState.EXECUTING
        self.drone.move(targetPosition)

    def isComplete(self):
        print("actual: " + str(self.drone.actualPosition))
        print("target: " + str(self.drone.targetPosition))
        print(str(self.drone.actualPosition == self.drone.targetPosition))
        if self.drone.actualPosition == self.drone.targetPosition:
            self.isCompleted = True

    def __repr__(self):
        ret = "\n\t<MovementTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
