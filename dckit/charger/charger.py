from dckit.charger.charger_state import ChargerState

class Charger(object):

    #Private Variables
    __coordinates = (0 , 0)
    __state = ChargerState.AVAILABLE
    __drone = None

    #Public Variables
    name = "Charger"

    #Initialize
    def __init__(self, name):
        super(Charger, self).__init__()
        self.name = name
    
    #Public Methods
    def initialize(self):
        self.starting_position = self.get_position()
        self.position = self.starting_position

    def setCoordinates(self, x, y):
        self.coordinates = (x, y)

    def getCoordinates():
        return self.coordinates

    def isAvaliable():
        return __state == ChargerState.AVAILABLE

    def chargeDrone(drone):
        if(isAvaliable()):
            __drone = drone
            __state = ChargerState.OCCUPIED
        else:
            raise Exception('Charger occupied', 'Charger is not allowed to recharge 2 drones simultaneously')

