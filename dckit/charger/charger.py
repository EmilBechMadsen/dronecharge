from dckit.charger.charger_state import ChargerState
from dckit.common.event import Event
import threading

class Charger(object):

    #Private Variables
    __coordinates = (0 , 0, 0)
    __state = ChargerState.AVAILABLE
    __drone = None

    #Public Variables
    name = "Charger"

    #Initialize
    def __init__(self, name):
        super(Charger, self).__init__()
        self.name = name

        #Hook up event handlers
        self.DroneReservedCharger += self.__onDroneReservedCharger
        self.DroneLanaded += self.__onDroneLanaded
        self.DroneRecharged += self.__onDroneRecharged
    
    #Public Methods
    def initialize(self):
        self.starting_position = self.get_position()
        self.position = self.starting_position

    def setCoordinates(self, x, y, z):
        self.coordinates = (x, y, z)

    def getCoordinates(self):
        return self.coordinates

    def getState(self):
        return self.__state;

    def isAvaliable(self):
        return self.__state == ChargerState.AVAILABLE

    def chargeDrone(self, drone):
        if(self.isAvaliable()):
            __drone = drone
            self.DroneReservedCharger([drone])
            #t = threading.Timer(5.0, self.DroneLanaded.trigger, [drone])
            #t = threading.Timer(14 * 60.0, self.DroneLanaded.trigger, [drone])

            #self.DroneRecharged([drone])

        else:
            raise Exception('Charger occupied', 'Charger is not allowed to recharge 2 drones simultaneously')

    def fireEvent(self, event):
        self.__DroneReservedCharger([self.__drone])

    #Events
    DroneReservedCharger = Event("Drone Reserved Charger")
    DroneLanaded = Event("Drone Landed")
    DroneRecharged = Event("Drone Recharged")

    #Event handlers
    def __onDroneReservedCharger(self, drone):
        self.__state = ChargerState.RESERVED

    def __onDroneLanaded(self, drone):
        self.__state = ChargerState.OCCUPIED

    def __onDroneRecharged(self, drone):
        self.__state = ChargerState.AVAILABLE


