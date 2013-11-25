from dckit.drone_factory import DroneFactory
from dckit.charger.charger import Charger
from dckit.common.event import Event

class ChargerManager(object):

    #Private Variables
    __chargers = []
    __droneFactory = None

    #Initialize
    def __init__(self, droneFactory):
        super(ChargerManager, self).__init__()
        self.__droneFactory = droneFactory

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

        #Wire up event handers
        for charger in self.__chargers:
            #print charger
            charger.DroneRecharged += self.__droneFactory.returnDroneToAvaliablePool
    
    #Private Methods
    def __validateChargerPosition(self, charger):
        return True

    #Public Methods
    def addCharger(self, charger):
        if(self.__validateChargerPosition(charger)):
            self.__chargers.append(charger)
            self.__ChargerAdded([charger])

    def sendDroneToCharger(self, drone):
        self__chargers[0].chargeDrone(drone)

    #TODO
    def removeCharger(self, x, y):
        raise NotImplementedError("TODO - 'removeCharger' method is not implemented")

    #TODO
    def findClosestCharger(self, drone):
        raise NotImplementedError("TODO - 'findClosestCharger' method is not implemented")

    #Events
    __ChargerAdded = Event("ChargerAdded")

    #Event handlers
    def onChargerAdded(sender, charger):
        print 'Charger added to manager: %s' % charger.name



