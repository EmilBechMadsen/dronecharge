import sys
import time
import curses
import cflib
import cflib.crtp
from cflib.crazyflie import Crazyflie

# help(cflib)
def clamp(value, minimum, maximum):
	return sorted((value,minimum,maximum))[1]

cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()

for i in available:
	print("Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1]))

if len(available) < 2:
	print("No drone interface found!")
	sys.exit(0)

crazyflie = Crazyflie()
crazyflie.open_link("radio://0/10/250K")

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
stdscr.timeout(50)

stdscr.addstr(0,0,"Hit 'q' to quit")
stdscr.refresh()

roll = 0.0
pitch = 0.0
yawrate = 0
thrust = 20000

key = ''
while True:
    key = stdscr.getch()

    if key == ord('q'):
    	crazyflie.commander.send_setpoint(0.0, 0.0, 0.0, 0)
    	time.sleep(0.1)
    	crazyflie.close_link()
    	curses.endwin()
    	sys.exit(0)

    # thrust
    if key == curses.KEY_UP: 
        thrust += 1000
    elif key == curses.KEY_DOWN: 
        thrust -= 1000
    # emergency stop
    elif key == ord('s'):
    	thrust = 10000
    # yawrate
    elif key == ord(','):
    	yawrate -= 0.5 
    elif key == ord('.'):
    	yawrate = 0.0
    elif key == ord('/'):
    	yawrate += 0.5
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
    yawrate = clamp(yawrate, -10, 10)

    stdscr.addstr(1, 0, "Roll: {0}".format(roll))
    stdscr.addstr(2, 0, "Pitch: {0}".format(pitch))
    stdscr.addstr(3, 0, "Yawrate: {0}".format(yawrate))
    stdscr.addstr(4, 0, "Thrust: {0}".format(thrust))

    stdscr.addch(20,25,key)
    stdscr.redrawwin()
    stdscr.refresh()

    crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
    # time.sleep(0.05)


