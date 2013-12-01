from dckit import DCKit
from dckit.tasks.task import Task
from dckit.tasks.movement_task import MovementTask
from dckit.tasks.videorecord_task import VideoRecordTask
from dckit.drivers.realistic import RealisticDrone
from dckit.charger.charger import Charger
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dckit = DCKit()

# Growing Y is NORTH
# dckit.environment.setFrameOfReference((10, 10, 10))
# dckit.environment.setOrigin((5, 5, 0))
# dckit.environment.addCharger((5, 5, 0))

 # Initialize chargers
charger1 = Charger("TopLeftCharger")
charger1.setCoordinates(-200, -200, 0)

charger2 = Charger("TopRightCharger")
charger2.setCoordinates(-200, -180, 0)

charger3 = Charger("BottomRightCharger")
charger3.setCoordinates(10, 0, 0)

charger4 = Charger("BottomLeftCharger")
charger4.setCoordinates(0, 0, 0)

drone = RealisticDrone("Drone 1")
drone.charger = charger1
#drone.position = charger1.getCoordinates()
dckit.addDrone(drone)

drone2 = RealisticDrone("Drone 2")
drone2.charger = charger2
drone2.position = charger2.getCoordinates()
dckit.addDrone(drone2)

task = Task("Maintask")
subtask1 = MovementTask("1", (100, 1, 1))
subtask2 = Task(" ")
subtask3 = Task(" ")
subtask4 = MovementTask("6", (100, 100, 3))
subtask5 = Task(" ")
subtask6 = MovementTask("2", (-100, 50, 3))
subtask7 = MovementTask("5", (-80, 30, 10))
subtask8 = MovementTask("7", (-0, 10, 8))
subtask9 = MovementTask("4", (-0, 200, 10))
subtask10 = VideoRecordTask("3 - Video")

# Probably need some way for each subtask to know which
# parent-task it is under so we can reference it's drones and environment easily?

task.addSubtask(subtask1)
subtask2.addSubtask(subtask3)
subtask2.addSubtask(subtask4)
subtask3.addSubtask(subtask5)
subtask3.addSubtask(subtask7)
subtask5.addSubtask(subtask6)
subtask5.addSubtask(subtask10)
subtask5.addSubtask(subtask9)
task.addSubtask(subtask2)
task.addSubtask(subtask8)

dckit.addTask(task)
dckit.run(True)
# dckit
