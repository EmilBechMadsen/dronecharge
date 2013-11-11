class Charger(object):

    #Private Variables
    __coordinates = (0 , 0)
    __isAvaliable = True
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
        return __isAvaliable

    def chargeDrone(drone):
        if(isAvaliable()):
            __drone = drone
            __isAvaliable = false
        else:
            raise Exception('Charger occupied', 'Charger is not allowed to recharge 2 drones simultaneously')

