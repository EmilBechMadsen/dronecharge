import curses
import time
import sys
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

key = ''
while True:
    key = stdscr.getch()
    if key == ord('q'):
    	curses.endwin()
    	sys.exit(0)

    stdscr.addch(20,25,key)
    stdscr.refresh()
    if key == curses.KEY_UP: 
        stdscr.addstr(2, 20, "Up")
    elif key == curses.KEY_DOWN: 
        stdscr.addstr(3, 20, "Down")

    time.sleep(0.1)

curses.endwin()
