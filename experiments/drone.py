import time
import cflib
import cflib.crtp
from cflib.crazyflie import Crazyflie
from crazylog import LogVariable, LogConfig
from pid import PID


class Drone(object):
    def __init__(self, autoconnect=True):
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.thrust = 10000
        self.bat = 0.0

        self.stabilizer_roll = 0.0
        self.stabilizer_pitch = 0.0
        self.stabilizer_yaw = 0.0

        # Angle to the Y axis
        self.angle = 0.0

        self.pid_roll = PID(Kp=1, Kd=0.4, Ki=0.00025)
        self.pid_pitch = PID(Kp=1, Kd=0.4, Ki=0.00025)
        self.pid_yaw = PID(Kp=10.0, Kd=0.0, Ki=0.0)
        self.pid_thrust = PID(Kp=0.1, Kd=0.1, Ki=0.00025)

        self.cf = Crazyflie(link=None, ro_cache="./cache", rw_cache="./cache")
        self.cf.connectSetupFinished.add_callback(self.setup_finished)
        self.init_interfaces()
        self.connect()

    def init_interfaces(self):
        # logging.basicConfig(level=logging.DEBUG)
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()

        for i in available:
            text = "Interface with URI [%s] found and name/comment [%s]"
            print(text.format(i[0], i[1]))

        if len(available) < 2:
            print("No drone interface found!")
            # sys.exit(0)

    def connect(self, interface="radio://0/10/250K"):
        self.cf.open_link(interface)

    def disconnect(self):
        self.stop()
        time.sleep(0.1)
        self.cf.close_link()

    def reconnect(self, interface="radio://0/10/250K"):
        self.disconnect()
        self.connect(interface)

    def setup_finished(self, linkURI):
        accel_log_conf = LogConfig("Stabilizer", 10)
        accel_log_conf.addVariable(LogVariable("stabilizer.roll", "float"))
        accel_log_conf.addVariable(LogVariable("stabilizer.pitch", "float"))
        accel_log_conf.addVariable(LogVariable("stabilizer.yaw", "float"))

        bat_log_conf = LogConfig("Battery", 100)
        bat_log_conf.addVariable(LogVariable("pm.vbat", "float"))

        accel_log = self.cf.log.create_log_packet(accel_log_conf)
        bat_log = self.cf.log.create_log_packet(bat_log_conf)

        if accel_log is not None:
            accel_log.dataReceived.add_callback(self.accel_data_callback)
            accel_log.start()
        else:
            print("acc.x/y/z not found in TOC")

        if bat_log is not None:
            bat_log.dataReceived.add_callback(self.bat_data_callback)
            bat_log.start()
        else:
            print("pm.bat not found in TOC")

    def accel_data_callback(self, data):
        self.stabilizer_roll = data['stabilizer.roll']
        self.stabilizer_pitch = data['stabilizer.pitch']
        self.stabilizer_yaw = data['stabilizer.yaw']

    def bat_data_callback(self, data):
        self.bat = data['pm.bat']

    def set_point(self, roll, pitch, yawrate, thrust):
        self.cf.commander.send_setpoint(roll, pitch, yawrate, thrust)

    def stop(self):
        self.thrust = 10000

    def update(self, roll_error=None, pitch_error=None, yaw_error=None,
               thrust_error=None):

        if roll_error:
            self.roll = self.pid_roll.GenOut(roll_error)

        if pitch_error:
            self.pitch = self.pid_pitch.GenOut(pitch_error)

        if yaw_error:
            self.yaw = self.pid_yaw.GenOut(yaw_error)

        if thrust_error:
            self.thrust = self.pid_thrust.GenOut(thrust_error)

        self.set_point(self.roll, self.pitch, self.yaw, self.thrust)
