from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep, time

from sr import Robot

from movements import *
from position import *
from strategy import *

def get_directions_for_XY(robot, x, y):
    """
    Returns angle to turn and the distance to move.
    """
    return 0, 0


def main():
    robot.position = Tracker(robot.zone)
    print 'Start position:'
    print '   ', (robot.position.x, robot.position.y), robot.position.angle
    
    marker = scan_corner(robot, robot.zone)
    line_up_to(marker, robot)
    move_till_touch(robot)
    
    print 'End Position:\n   '
    print '   ', (robot.position.x, robot.position.y)

robot = Robot()

world_exists = True
while world_exists:
    main()
    sleep(5)
