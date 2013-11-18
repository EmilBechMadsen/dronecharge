import unittest
from dckit import DCKit
from dckit.drone import Drone
import logging


logger = logging.getLogger(__name__)


class DroneTest(unittest.TestCase):
    def setUp(self):
        self.dckit = DCKit()

    def tearDown(self):
        pass

    def test_capabilities(self):
        drone = Drone("Drone 1")

        available_capabilities = [
            "move",
            "cam",
            "microphone"
        ]

        required_capabilities = [
            "move",
            "microphone"
        ]

        drone.capabilities = available_capabilities
        self.assertTrue(drone.hasCapabilities(required_capabilities), "Has all the required_capabilities")

        required_capabilities = [
            "move",
            "microphone",
            "gps"
        ]

        self.assertFalse(drone.hasCapabilities(required_capabilities), "Drone lacks GPS")
