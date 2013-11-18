from dckit.enum import Enum


class TaskState(Enum):
    READY = 0
    EXECUTING = 1
    COMPLETE = 2


