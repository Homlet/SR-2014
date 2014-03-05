from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep, time

from sr import Robot

from movements import Tracker
from strategy import line_up_to_marker, scan_corner


def main():
    robot.position = Tracker(robot.zone)
    print 'Start\n    x = %.1f y = %.1f theta = %.1f' % (*robot.position)
    # print '   ', (robot.position.x, robot.position.y), robot.position.angle
    
    # Main strategy goes here:
    marker = scan_corner(robot, robot.zone)
    line_up_to_marker(robot, marker)
    move_till_touch(robot)
    
    print 'End\n    x = %.1f y = %.1f theta = %.1f' % (*robot.position)
    # print '   ', (robot.position.x, robot.position.y), robot.position.angle

robot = Robot()

world_exists = True
while world_exists:
    main()
    sleep(5)
