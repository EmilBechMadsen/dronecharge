from dckit.charger.charger import Charger

class ChargerManager(object):

    #Private Variables
    __chargers = []

    #Public Variables

    #Initialize
    def __init__(self):
        super(ChargerManager, self).__init__()
        # Initialize chargers
        charger1 = Charger("TopLeftCharger")
        charger1.setCoordinates(0, 10)
        self.addCharger(charger1)

        charger2 = Charger("TopRightCharger")
        charger2.setCoordinates(10, 10)
        self.addCharger(charger2)

        charger3 = Charger("BottomRightCharger")
        charger3.setCoordinates(10, 0)
        self.addCharger(charger3)

        charger4 = Charger("BottomLeftCharger")
        charger4.setCoordinates(0, 0)
        self.addCharger(charger4)
    
    #Private Methods
    def __validateChargerPosition(self, charger):
        return True

    #Public Methods
    def addCharger(self, charger):
        if(self.__validateChargerPosition(charger)):
            self.__chargers.append(charger)

    #TODO
    def removeCharger(self, x, y):
        raise NotImplementedError("TODO - 'removeCharger' method is not implemented")

    #TODO
    def findClosestCharger(self, drone):
        raise NotImplementedError("TODO - 'findClosestCharger' method is not implemented")


