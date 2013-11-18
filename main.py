from dckit import DCKit
from dckit.tasks.task import Task
from dckit.tasks.movement_task import MovementTask
from dckit.drivers.ideal import IdealDrone
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dckit = DCKit()

# Growing Y is NORTH
# dckit.environment.setFrameOfReference((10, 10, 10))
# dckit.environment.setOrigin((5, 5, 0))
# dckit.environment.addCharger((5, 5, 0))

for i in range(4):
    drone = IdealDrone("Drone " + str(i))
    dckit.addDrone(drone)

task = Task("Maintask")
subtask1 = MovementTask("subtask1", (1, 1, 1))
subtask2 = Task("subtask2", (2, 2, 2))
subtask3 = Task("subtask3", (3, 3, 3))
subtask4 = MovementTask("subtask4", (3, 3, 3))
subtask5 = Task("subtask5", (3, 3, 3))
subtask6 = MovementTask("subtask6", (3, 3, 3))

# Probably need some way for each subtask to know which
# parent-task it is under so we can reference it's drones and environment easily?
subtask1.setDrone(drone)
subtask2.setDrone(drone)
subtask3.setDrone(drone)
subtask4.setDrone(drone)
subtask5.setDrone(drone)
subtask6.setDrone(drone)

task.addSubtask(subtask1)
subtask2.addSubtask(subtask3)
subtask2.addSubtask(subtask4)
subtask3.addSubtask(subtask5)
subtask5.addSubtask(subtask6)
task.addSubtask(subtask2)

dckit.addTask(task)
dckit.run(True)
# dckit
