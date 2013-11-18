import unittest
from dckit import DCKit
from dckit.drivers.ideal import IdealDrone


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.dckit = DCKit()

    def tearDown(self):
        pass

    def test_replaceDroneIfNeeded(self):
        drone1 = IdealDrone("Drone 1")
        drone2 = IdealDrone("Drone 2")

        drone1.capabilities = ["move"]
        drone2.capabilities = ["move", "cam"]

        self.dckit.addDrone(drone1)
        self.dckit.addDrone(drone2)

        drone1.battery_level = 0.19
        
        drone = self.dckit.environment.replaceDroneIfNeeded(drone1, set([]))

        self.assertEqual(drone, drone2, "Replaced with the right drone")

        drone1.battery_level = 0.8
        drone = self.dckit.environment.replaceDroneIfNeeded(drone1, set(["cam"]))
        # print(drone)
        # print(drone1)
        # self.assertEqual(drone, drone2, "Replace with drone with right caps")

    def test_getDrone(self):
        pass
        
