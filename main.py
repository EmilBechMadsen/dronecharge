from dckit import DCKit
from dckit.drivers.crazyflie import Crazyflie
from dckit.environment import Environment
from dckit.task import Task

a2b = DCKit()

environment = Environment()

# Growing Y is NORTH
environment.setFrameOfReference(10, 10, 10)
environment.setOrigin(5, 5, 0)
environment.addOharger(5, 5, 0)

for i in range(4):
    drone = Crazyflie("Drone " + str(i))
    environment.addDrone(drone)

task = Task("Record in a square")

rectask = RecordingTask("Start Recording")
task.add(rectask)

movetask = MovementTask("Move to A", (0,1,1))
task.add(moveTask)


task.Start()

foreach task in subtasks:
task.run(drone)

subtask = MovementTask("Move")
# subtask.addDrone("Drone 1")
# subtask.addDroneGroup(1)
subtask.moveRelative(0, 0, 1)

subtask = AVTask("Turn on video and bla")




task.addSubtask(subtask)

environment.setTask(task)

a2b.setEnvironment(environment)
a2b.start(timeout=2 * 60 * 60)
