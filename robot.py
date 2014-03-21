from time import sleep

from sr import Robot

from movements import Tracker, turn, move_straight, prepare_for_grab, grab
from strategy import (line_up_to_marker, scan_corner, move_till_touch,
    move_to_point)
from mechanics import raise_arms, lower_arms, open_arms, close_arms

def use_arms(robot):
    while True:
        sleep(2)
        print('raise')
        raise_arms(robot)
        sleep(2)
        print('lower')
        lower_arms(robot)
        sleep(2)
        print('open')
        open_arms(robot)
        sleep(2)
        print('close')
        close_arms(robot)
        print "cycled"

def get_to_marker(robot):
    marker = scan_corner(robot, robot.zone)[0]
    line_up_to_marker(robot, marker)
    move_till_touch(robot)

def main():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    while 1:
        try:
            # get_to_marker()
            use_arms(robot)
        except:
            print 'There was an error. Restarting in 2s.'
            sleep(2)
            continue

# def failsafe_main():
#     """I sold my soul to write this function."""
#     try:
#         main()
#     except:
#         failsafe_main()

main()
