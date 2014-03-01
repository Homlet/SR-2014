from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep, time

from sr import Robot

from position import Tracker, 
from strategy import *


def main():
    robot.position = Tracker(robot.zone)
    print 'Start position:'
    print '   ', (robot.position.x, robot.position.y), robot.position.angle
    
	# Main strategy goes here:
    marker = scan_corner(robot, robot.zone)
    line_up_to(marker, robot)
    move_till_touch(robot)
    
    print 'End Position:'
    print '   ', (robot.position.x, robot.position.y), robot.position.angle

robot = Robot()

world_exists = True
while world_exists:
    main()
    sleep(5)
