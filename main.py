from dckit import DCKit
from dckit.tasks.task import Task
from dckit.tasks.movement_task import MovementTask
from dckit.tasks.takeoff_task import TakeoffTask
from dckit.tasks.landing_task import LandingTask
from dckit.drivers.ardrone import ARDrone
from dckit.drivers.realistic import RealisticDrone
from dckit.charger.charger import Charger
import logging
import cv2
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dckit = DCKit()

 # Initialize chargers
charger1 = Charger("TopLeftCharger")
charger1.setCoordinates(0, 0, 0)

drone = ARDrone("Drone 1")
drone.charger = charger1
drone.position = charger1.getCoordinates()
drone.target = charger1.getCoordinates()
# drone.hue_range = (70, 100)
time.sleep(1)
dckit.addDrone(drone)

task = Task("Maintask")
subtask1 = TakeoffTask()

sqsize = 130

movements = Task("Move in square")
subtask2 = MovementTask("1", (sqsize, sqsize, 1))
subtask3 = MovementTask("2", (sqsize, -sqsize, 1))
subtask4 = MovementTask("3", (-sqsize, -sqsize, 1))
subtask5 = MovementTask("4", (-sqsize, sqsize, 1))
subtask6 = LandingTask()

task.addSubtask(subtask1)
movements.addSubtask(subtask2)
movements.addSubtask(subtask3)
movements.addSubtask(subtask4)
movements.addSubtask(subtask5)
task.addSubtask(movements)
task.addSubtask(subtask6)



dckit.addTask(task)

dckit.run(True)
