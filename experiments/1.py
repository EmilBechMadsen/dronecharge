import sys
import math
import time
import logging
import signal
import cv2
import freenect
from matplotlib.pylab import *
import cflib
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import Log, LogTocElement

class LogConfig():
    def __init__(self, configname, period=0, filename=""):
        self.period = period
        self.variables = []
        self.configName = configname
        self.configFileName = filename
        self.datarangeMin = 0
        self.datarangeMax = 0

    def addVariable(self, var):
        self.variables.append(var)

    def setPeriod(self, period):
        self.period = period

    def setDataRange(self, minVal, maxVal):
        self.datarangeMin = minVal
        self.datarangeMax = maxVal

    def getVariables(self):
        return self.variables

    def getName(self):
        return self.configName

    def getDataRangeMin(self):
        return self.datarangeMin

    def getDataRangeMax(self):
        return self.datarangeMax

    def getPeriod(self):
        return self.period

    def __str__(self):
        return ("LogConfig: name=%s, period=%d, variables=%d" %
                (self.configName, self.period, len(self.variables)))


class LogVariable():
    """A logging variable"""

    TOC_TYPE = 0
    MEM_TYPE = 1

    def __init__(self, name="", fetchAs="uint8_t", varType=0, storedAs="",
                 address=0):
        self.name = name
        self.fetchAs = LogTocElement.get_id_from_cstring(fetchAs)
        if (len(storedAs) == 0):
            self.storedAs = self.fetchAs
        else:
            self.storedAs = LogTocElement.get_id_from_cstring(storedAs)
        self.address = address
        self.varType = varType
        self.fetchAndStoreageString = fetchAs
        self.storedAsString = storedAs
        self.fetchAsString = fetchAs

    def setName(self, name):
        """Set the name"""
        self.name = name

    def setTypes(self, storeAs, fetchAs):
        """
        Set the type the variable is stored as in the Crazyflie and the type it
        should be fetched as.
        """
        self.fetchAs = fetchAs
        self.storeAs = storeAs

    def isTocVariable(self):
        """
        Return true if the variable should be in the TOC, false if raw memory
        variable
        """
        return self.varType == LogVariable.TOC_TYPE

    def setAddress(self, addr):
        """Set the address in case of raw memory logging."""
        self.address = addr

    def getName(self):
        """Return the variable name"""
        return self.name

    def getStoredAs(self):
        """Return the type the variable is stored as in the Crazyflie"""
        return self.storedAs

    def getFetchAs(self):
        """Return the type the variable should be fetched as."""
        return self.fetchAs

    def getAddress(self):
        """Return the address in case of memory logging."""
        return self.address

    def getVarType(self):
        """Get the variable type"""
        return self.varType

    def getStoredFetchAs(self):
        """Return what the variable is stored as and fetched as"""
        return (self.fetchAs | (self.storedAs << 4))

    def setFetchAndStorageString(self, s):
        """Set the fetch and store string"""
        self.fetchAndStoreageString = s

    def getFetchAndStorageString(self):
        """Return the fetch and store string"""
        return self.fetchAndStoreageString

    def __str__(self):
        return ("LogVariable: name=%s, store=%s, fetch=%s" %
                (self.name, LogTocElement.get_cstring_from_id(self.storedAs),
                 LogTocElement.get_cstring_from_id(self.fetchAs)))

class PID:

    def __init__(self, P=1.0, I=0.0, D=10.0, Derivator=0, Integrator=0,
                 Integrator_max=300, Integrator_min=-200, set_point=0.0,
                 power=1.0):

        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.power = power
        self.Integrator=Integrator
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min
        self.last_error = 0.0
        self.last_value = 0.0

        self.set_point=set_point
        self.error=0.0

    def update(self,current_value):
        """
        Calculate PID output value for given reference input and feedback
        """

        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        if (self.last_value >= current_value):
            change = self.error - self.last_error
        else:
            change = 0.0

        if self.error > 0.0:
            self.I_value = self.Integrator * self.Ki
        else:
            self.I_value = (self.Integrator * self.Ki)


        #self.D_value = self.Kd * ( self.error - self.Derivator)
        self.D_value = self.Kd * change
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error/200.0

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.last_error = self.error
        self.last_value = current_value

        PID = self.P_value + self.I_value + self.D_value

        return PID

    def set_point(self,set_point):
        """Initilize the setpoint of PID"""
        self.set_point = set_point
        self.Integrator=0
        self.Derivator=0

class PID_RP:

    def __init__(self, P=1.0, I=0.0, D=10.0, Derivator=0, Integrator=0,
                 Integrator_max=20000, Integrator_min=-20000, set_point=0.0,
                 power=1.0):

        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.power = power
        self.Integrator=Integrator
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min
        self.last_error = 0.0
        self.last_value = 0.0

        self.set_point=set_point
        self.error=0.0

    def update(self,current_value):
        """
        Calculate PID output value for given reference input and feedback
        """

        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        change = self.error - self.last_error
        
        self.I_value = self.Integrator * self.Ki

        #self.D_value = self.Kd * ( self.error - self.Derivator)
        self.D_value = self.Kd * change
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.last_error = self.error
        self.last_value = current_value

        PID = self.P_value + self.I_value + self.D_value

        return PID

    def set_point(self,set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.Integrator=0
        self.Derivator=0


# help(cflib)
def clamp(value, minimum, maximum):
    return sorted((value,minimum,maximum))[1]

accel_log = None
bat_log = None
def setup_finished(linkURI):

    accel_log_conf = LogConfig("Stabilizer", 10)
    accel_log_conf.addVariable(LogVariable("stabilizer.roll", "float"))
    accel_log_conf.addVariable(LogVariable("stabilizer.pitch", "float"))
    accel_log_conf.addVariable(LogVariable("stabilizer.yaw", "float"))

    bat_log_conf = LogConfig("Battery", 100)
    bat_log_conf.addVariable(LogVariable("pm.vbat", "float"))

    accel_log = crazyflie.log.create_log_packet(accel_log_conf)
    bat_log = crazyflie.log.create_log_packet(bat_log_conf)

    if accel_log is not None:
        accel_log.dataReceived.add_callback(accel_data)
        accel_log.start()
    else:
        print("acc.x/y/z not found in TOC")

    if bat_log is not None:
        bat_log.dataReceived.add_callback(bat_data)
        bat_log.start()
    else:
        print("pm.bat not found in TOC")

def accel_data(data):
    global _roll
    global _pitch
    global _yaw
    global window

    _roll = data['stabilizer.roll']
    _pitch = data['stabilizer.pitch']
    _yaw = data['stabilizer.yaw']
    

def bat_data(data):
    global _bat
    _bat = data['pm.bat']

# logging.basicConfig(level=logging.DEBUG)
cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()

for i in available:
    print("Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1]))

if len(available) < 2:
    print("No drone interface found!")
    # sys.exit(0)

crazyflie = Crazyflie(link=None, ro_cache="./cache", rw_cache="./cache")
crazyflie.connectSetupFinished.add_callback(setup_finished)
crazyflie.open_link("radio://0/10/250K")

window = cv2.namedWindow("win")
cv2.moveWindow("win", 800, 0)

_bat = 0.0
_roll = 0.0
_pitch = 0.0
_yaw = 0.0
roll = 0.0
pitch = 0.0
yawrate = 0
thrust = 10000

pid_p = 1.0
pid_i = 0.05
pid_d = 0

roll_pid = PID_RP(P=pid_p, D=pid_d, I=pid_i, set_point=0.0)
pitch_pid = PID_RP(P=pid_p, D=pid_d, I=pid_i, set_point=0.0)
yaw_pid = PID(P=0.5, I=0.00025, D=0.5)

def update_yaw_pid_p(value):
    global yaw_pid
    print(float(value) / 100.0)
    yaw_pid.kp = float(value) / 100.0

def update_yaw_pid_i(value):
    global yaw_pid
    yaw_pid.ki = float(value) / 100.0

def update_yaw_pid_d(value):
    global yaw_pid
    yaw_pid.kd = float(value) / 100.0

# control_win = cv2.namedWindow("Control Panel")
# cv2.createTrackbar("Yaw P", "Control Panel", 0, 100, update_yaw_pid_p)
# cv2.createTrackbar("Yaw I", "Control Panel", 0, 100, update_yaw_pid_p)
# cv2.createTrackbar("Yaw D", "Control Panel", 0, 100, update_yaw_pid_p)

ion()                           # interaction mode needs to be turned off
 
x = arange(0, 100, 1)         # we'll create an x-axis from 0 to 2 pi
yaw_error = arange(0, 100, 1, dtype="float")
yaw_line, = plot(x,x, label="Yaw")               # this is our initial plot, and does nothing
yaw_line.axes.set_ylim(-200,200)        # set the range for our plot
 
roll_error = arange(0, 100, 1, dtype="float")
roll_line, = plot(x,x, label="Roll")               # this is our initial plot, and does nothing
roll_line.axes.set_ylim(-15,15)        # set the range for our plot

pitch_error = arange(0, 100, 1, dtype="float")
pitch_line, = plot(x,x, label="Pitch")               # this is our initial plot, and does nothing
pitch_line.axes.set_ylim(-15,15)        # set the range for our plot

legend()

starttime = time.time()         # this is our start time
t = 0                           # this is our relative start time

key = ''
while True:
    key = cv2.waitKey(1)

    if key == ord('q'):
        crazyflie.commander.send_setpoint(0.0, 0.0, 0.0, 0)
        time.sleep(0.1)
        crazyflie.close_link()
        break

    if key == ord('r'):
        crazyflie.commander.send_setpoint(0.0, 0.0, 0.0, 0)
        time.sleep(0.1)
        crazyflie.close_link()
        time.sleep(0.1)
        crazyflie.open_link("radio://0/10/250K")

    # thrust
    if key == 63232: 
        thrust += 1000
    elif key == 63233: 
        thrust -= 1000
    # emergency stop
    elif key == ord('s'):
        thrust = 10000
    # yawrate
    elif key == ord(','):
        yawrate = -200.0 
    elif key == ord('.'):
        yawrate = 0.0
    elif key == ord('/'):
        yawrate = 200.0
    # roll
    elif key == ord(','):
        roll -= 0.1 
    elif key == ord('.'):
        roll = 0.0
    elif key == ord('/'):
        roll += 0.1
    # pitch
    elif key == ord(','):
        pitch -= 0.1 
    elif key == ord('.'):
        pitch = 0.0
    elif key == ord('/'):
        pitch += 0.1

    thrust = clamp(thrust, 10000, 60000)
    yawrate = clamp(yawrate, -360, 360)

    rollrate = abs(_roll) * 0.4
    pitchrate = abs(_pitch) * 0.4
    yawrate2 = abs(_yaw) * 0.4

    if _roll > 0:
        roll = -rollrate

    if _roll < 0:
        roll = rollrate

    if _pitch > 0:
        pitch = -pitchrate

    if _pitch < 0:
        pitch = pitchrate

    if _yaw > 0:
        yawrate = -yawrate2

    if _yaw < 0:
        yawrate = yawrate2

    yawrate = 0 #yaw_pid.update(_yaw)
    pitch = pitch_pid.update(_pitch)
    roll = roll_pid.update(_roll)

    crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
    # time.sleep(0.05)
    
    image = np.zeros((480,640))
    # image = freenect.sync_get_video()[0]
    # image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)

    # ret, thresh = cv2.threshold(image[:,:,0], 150, 255, cv2.THRESH_BINARY)

    # cv2.imshow("H", thresh)
    # cv2.imshow("S", image[:,:,1])
    # # cv2.imshow("V", image[:,:,2])


    yaw_error = np.append(yaw_error, yaw_pid.error)[1:]
    roll_error = np.append(roll_error, roll_pid.error)[1:]
    pitch_error = np.append(pitch_error, pitch_pid.error)[1:]

    # update the plot data
    yaw_line.set_ydata(yaw_error)           
    roll_line.set_ydata(roll_error)
    pitch_line.set_ydata(pitch_error)

    draw()  

    cv2.putText(image, "Roll  : {0:.4} {1:.4}".format(roll, _roll), (10,20), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,255))
    cv2.putText(image, "Pitch : {0:.4} {1:.4}".format(pitch, _pitch), (10,40), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,255))
    cv2.putText(image, "Yaw   : {0:.4} {1:.4}".format(float(yawrate), _yaw), (10,60), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,255))
    cv2.putText(image, "Thrust: {0}".format(thrust), (10,80), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,255))
    cv2.putText(image, "Bat   : {0}".format(_bat), (10,100), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,255))

    cv2.putText(image, "Error   : {0}".format(yaw_pid.error), (10,120), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,255))
    
    cv2.imshow("win", image)
