from time import sleep

from sr import Robot

from movements import Tracker
from strategy import (line_up_to_marker, scan_corner, move_till_touch,
    move_to_point)

def main():
    robot.position = Tracker(robot.zone)
    move_to_point(robot, 3, 3)
    return
    p = robot.position
    print 'Start\n    x = %.1f y = %.1f theta = %.1f' % (p.x, p.y, p.theta)
    
    # Main strategy goes here:
    marker = scan_corner(robot, robot.zone)
    line_up_to_marker(robot, marker)
    move_till_touch(robot)
    
    p = robot.position
    print 'End\n    x = %.1f y = %.1f theta = %.1f' % (p.x, p.y, p.theta)

robot = Robot()

world_exists = True
while world_exists:
    main()
    sleep(30)
