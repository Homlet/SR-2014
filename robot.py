from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep, time

from sr import Robot

from movements import *
from position import *
from strategy import *

def main():
    robot.position = Tracker(robot.zone)
    print 'Start position:'
    print '   ', (robot.position.x, robot.position.y), robot.position.angle
    
    scan_corner(robot)
    line_up_to(marker, robot)
    move_till_touch(robot)
    
    print 'End Position:\n   '
    print '   ', (robot.position.x, robot.position.y)

robot = Robot()

world_exists = True
while world_exists:
    main()
    sleep(5)
