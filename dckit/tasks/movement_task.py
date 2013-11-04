from dckit.tasks.task import Task, TaskState


class MovementTask(Task):
    def __init__(self, name, targetPosition):
        super(MovementTask, self).__init__(name)

        self.isCompleted = False
        self.targetPosition = targetPosition

    def start(self):
        self.state = TaskState.EXECUTING

        self.isCompleted = True

    def isComplete(self):
        return self.isCompleted

    def __repr__(self):
        ret = "\n\t<MovementTask (" + self.name + ") "
        ret += " State: " + str(self.state)
        if len(self.subtasks):
            ret += "\n\t" + str(self.subtasks) + "\n\t"

        return ret
