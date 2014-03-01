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
    x0, y0, theta = robot.position.x, robot.position.y, robot.position.angle
    dx = x - x0
    dy = y - y0
    dist = sqrt(dx*dx + dy*dy)
    gamma = atan2(dx, dy)
    alpha = gamma - theta
    print 'theta = %.1f' % (theta)
    print 'turn:%.1f' % (alpha)
    return dist, alpha

def nick_main():
    robot = Robot()
    d = 2.2
    significantPoints = [(d, d), (8-d, d), (8-d, 8-d), (d, 8-d)]
    ourZone = robot.zone
    robot.position = Tracker(ourZone)
    dist, alpha = get_directions_for_XY(robot, *significantPoints[ourZone])
    # turn(robot, alpha)
    # move_straight(robot, dist)

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
