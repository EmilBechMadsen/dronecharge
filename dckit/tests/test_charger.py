import unittest
from dckit.charger.charger import Charger
from dckit.drone import Drone
from dckit.drivers.ideal import IdealDrone
from dckit.charger.charger_state import ChargerState

class ChargerTest(unittest.TestCase):

    __charger = None
    __drone = None

    def setUp(self):
        self.__charger = Charger("TopLeftCharger")
        self.__charger.setCoordinates(0, 10)
        self.__drone = IdealDrone("Drone")

    def tearDown(self):
        self.__charger = None
        self.__drone = None

    def test_afterInitializingChargerShouldBeInAvaliableState(self):
        #Initialize

        #Execute
        chargerState = self.__charger.getState()

        #Assert
        self.assertEqual(chargerState, ChargerState.AVAILABLE, "Charger is alwayas in Avaliable state after initilized")

    def test_afterInitializingChargerShouldBeInAvaliableState(self):
        #Initialize
        self.__charger.chargeDrone(self.__drone)

        #Execute
        chargerState = self.__charger.getState()

        #Assert
        self.assertEqual(chargerState, ChargerState.RESERVED, "After assigning drone to charger, charger should switch to Reserved state")

if __name__ == "__main__":
    unittest.main()
