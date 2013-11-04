from dckit import DCKit
from dckit.environment import Environment
from dckit.tasks.task import Task
from dckit.tasks.movement_task import MovementTask
from dckit.drivers.ideal import Ideal

from pprint import pprint

dckit = DCKit()

environment = Environment()

# Growing Y is NORTH
environment.setFrameOfReference((10, 10, 10))
environment.setOrigin((5, 5, 0))
environment.addCharger((5, 5, 0))

for i in range(4):
    drone = Ideal("Drone " + str(i), environment)
    environment.addDrone(drone)

task = Task("Maintask")

subtask1 = MovementTask("subtask1", (1,1,1))
subtask2 = MovementTask("subtask2", (2,2,2))
subtask3 = MovementTask("subtask3", (3,3,3))
task.addSubtask(subtask1)
subtask2.addSubtask(subtask3)
task.addSubtask(subtask2)

pprint(task)

dckit.addTask(task)

# dckit.setEnvironment(environment)
dckit._main_loop()
# dckit
