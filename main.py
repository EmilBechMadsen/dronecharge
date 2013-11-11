from dckit import DCKit
from dckit.environment import Environment
from dckit.tasks.task import Task
from dckit.tasks.movement_task import MovementTask
from dckit.drivers.ideal import Ideal
from dckit.charger.charger_manager import ChargerManager

from pprint import pprint

dckit = DCKit()

environment = Environment()

# Growing Y is NORTH
environment.setFrameOfReference((10, 10, 10))
environment.setOrigin((5, 5, 0))

for i in range(4):
    drone = Ideal("Drone " + str(i), environment)
    environment.addDrone(drone)

#Initialize Charger Manager
chargerManager = ChargerManager()

task = Task("Maintask")

subtask1 = MovementTask("subtask1", (1,1,1))
subtask2 = MovementTask("subtask2", (2,2,2))
subtask3 = MovementTask("subtask3", (3,3,3))
subtask4 = MovementTask("subtask4", (3,3,3))
subtask5 = MovementTask("subtask5", (3,3,3))
subtask6 = MovementTask("subtask6", (3,3,3))
task.addSubtask(subtask1)
subtask2.addSubtask(subtask3)
subtask2.addSubtask(subtask4)
subtask3.addSubtask(subtask5)
subtask5.addSubtask(subtask6)
task.addSubtask(subtask2)

dckit.addTask(task)

print("Before loop")
print(task)

# dckit.setEnvironment(environment)
dckit._main_loop()
# dckit
