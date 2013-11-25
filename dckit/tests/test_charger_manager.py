import unittest
from dckit import DCKit
from dckit.tasks.task import Task, TaskState
from dckit.tasks.movement_task import MovementTask
from dckit.drivers.ideal import IdealDrone


class ChargerManagerTest(unittest.TestCase):

    dckit = None
    environment = None

    def setUp(self):
        self.dckit = DCKit()

    def tearDown(self):
        pass

    def test_evaluate1(self):
        pass
        #environment = Environment()
        # Growing Y is NORTH
        #environment.setFrameOfReference((10, 10, 10))
        #environment.setOrigin((5, 5, 0))
        #environment.addCharger((5, 5, 0))

        #self.__droneFactory = DroneFactory()
        #for i in range(4):
        #    drone = IdealDrone("Drone " + str(i), environment)
        #self.__chargerManager = ChargerManager(self.__droneFactory)

if __name__ == "__main__":
    unittest.main()
