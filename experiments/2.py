import time
import sys
import cflib
import cflib.crtp
from cflib.crazyflie import Crazyflie
from pprint import pprint

cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()

for i in available:
	print("Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1]))

if len(available) < 2:
	print("No drone interface found!")
	sys.exit(0)

crazyflie = Crazyflie()
crazyflie.open_link("radio://0/10/250K")

roll = 0.0
pitch = 0.0
yawrate = 0
thrust = 10001
crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)

time.sleep(0.1)
crazyflie.close_link()
