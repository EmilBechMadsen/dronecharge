import logging

class DroneManager(object):

    #Private variables
    __avaliableDronesPool = []
    __occupiedDronesPool = []
    __logger = logging.getLogger(__name__)

    #Initialize
    def __init__(self):
        super(DroneManager, self).__init__()

    #Public methods
    def addDrone(self, drone):
        self.__avaliableDronesPool.append(drone)

    def anyDroneReady(self):
        return len(self.__avaliableDronesPool) > 0

    def getDrone(self):
        if self.anyDroneReady():
            _drone = self.__avaliableDronesPool.pop(0)
            self.__occupiedDronesPool.append(_drone)
            return _drone
        else:
            __logger.warning("No avaliable drones in pool!")
    
    def getDrone(self, capabilities):
        self.refreshAvaliableDronesPool()
        capableDrones = []
        for drone in self.__avaliableDronesPool:
            if not drone.hasCapabilities(capabilities):
                caps = set(capabilities) - set(drone.capabilities)
                logger.info("Rejecting drone based on capabilities %s", caps)
                continue

            capableDrones.append(drone)

        if len(capableDrones) == 0:
            return None
        else:
            return sorted(capableDrones, key=lambda x: len(x.capabilities))[0]

    def getAllDrones(self):
        return self.__avaliableDronesPool + self.__occupiedDronesPool

    def refreshAvaliableDronesPool(self):
        for drone in self.__occupiedDronesPool:
            if drone.getBatteryLevel() >= 0.95:
                self.returnDroneToAvaliablePool(drone)
                
    def returnDroneToAvaliablePool(self, drone):       
        if(self.__occupiedDronesPool.count(drone) == 1 ):
            print 'Drone returned to avaliable pool: %s' % drone.name
            self.__occupiedDronesPool.remove(drone)
            self.__avaliableDronesPool.push(drone)

