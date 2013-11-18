class DroneFactory(object):

    #Private variables
    __avaliableDronesPool = []
    __occupiedDronesPool = []

    #Initialize
    def __init__(self):
        super(DroneFactory, self).__init__()

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
            raise Exception("No avaliable drones in pool!")
            
    def returnDroneToAvaliablePool(self, drone):
        print 'ChargerManager: return drone fired: %s' % drone.name
        if(self.__occupiedDronesPool.count(drone) == 1 ):
            self.__occupiedDronesPool.remove(drone)
            self.__avaliableDronesPool.push(drone)

