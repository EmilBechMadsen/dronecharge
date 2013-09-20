from dckit import DCKit
from dckit.drivers.crazyflie import Crazyflie
from dckit.environment import Environment
from dckit.task import Task

a2b = DCKit()

environment = Environment()

# Growing Y is NORTH
environment.set_frame_of_reference(10, 10, 10)
environment.set_origin(5, 5, 0)
environment.add_charger(5, 5, 0)

for i in range(4)
	drone = Crazyflie("Drone " + str(i))
	environment.add_drone(drone)

task = Task("Hover")

subtask = Task("Move")
# subtask.add_drone("Drone 1")
# subtask.add_drone_group(1)
subtask.move_relative(0, 0, 1)

task.add_subtask(subtask)

environment.set_task(task)

a2b.set_environment(environment)
a2b.start(timeout = 2 * 60 * 60)
