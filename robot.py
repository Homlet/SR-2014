from time import sleep
from traceback import print_exc

from sr import Robot

from movements import Tracker
from strategy import (line_up_to_marker, scan_corner, move_till_touch,
    move_to_point, get_marker_from_corner)


def main():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    while 1:
        try:
            get_marker_from_corner(robot, robot.zone)
        except:
            print_exc()
            print '\nRestarting in 2s...\n'
            sleep(2)


main()
