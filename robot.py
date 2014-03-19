from time import sleep

from sr import Robot

from movements import Tracker, turn, move_straight, prepare_for_grab, grab
from strategy import (line_up_to_marker, scan_corner, move_till_touch,
    move_to_point)
from mechanics import raise_arms, lower_arms()

def main():
    robot.position = Tracker(robot.zone)
    
    p = robot.position
    print 'Start\n    x = %.1f y = %.1f theta = %.1f' % (p.x, p.y, p.theta)
    
    # Main strategy goes here:
    # marker = scan_corner(robot, robot.zone)
    # line_up_to_marker(robot, marker)
    # move_till_touch(robot)
    for i in range(2):
        turn(robot)
        sleep(2)
    
    move_straight(robot, 1)
    
    p = robot.position
    print 'End\n    x = %.1f y = %.1f theta = %.1f' % (p.x, p.y, p.theta)

robot = Robot()

# def failsafe_main():
#     """I sold my soul to write this function."""
#     try:
#         main()
#     except:
#         failsafe_main()

#main()


while True:
    lower_arms(robot)
    raise_arms(robot)