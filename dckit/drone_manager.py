import logging


logger = logging.getLogger(__name__)
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
        # logger.info("Drones available: %s", len(self.__avaliableDronesPool))
        return len(self.__avaliableDronesPool) > 0
    
    def getDrone(self, capabilities):
        self.refreshAvaliableDronesPool()
        # logger.info("Drones available: %s", len(self.__avaliableDronesPool))
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
            newDrone = sorted(capableDrones, key=lambda x: len(x.capabilities))[0]
            self.__occupiedDronesPool.append(newDrone)
            self.__avaliableDronesPool.remove(newDrone)
            return newDrone

    def getAllDrones(self):
        return self.__avaliableDronesPool + self.__occupiedDronesPool

    def stopAllDrones(self):
        logger.info("Stopping all drone control loops")
        for drone in self.getAllDrones():
            drone.stopControlLoop()

    def refreshAvaliableDronesPool(self):
        for drone in self.__occupiedDronesPool:
            if drone.getBatteryLevel() >= 0.95:
                self.returnDroneToAvaliablePool(drone)
                
    def returnDroneToAvaliablePool(self, drone):       
        if(self.__occupiedDronesPool.count(drone) == 1 ):
            print 'Drone returned to avaliable pool: %s' % drone.name
            self.__occupiedDronesPool.remove(drone)
            self.__avaliableDronesPool.append(drone)

