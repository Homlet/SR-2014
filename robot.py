from time import sleep
from traceback import print_exc
from math import pi

from sr import Robot

from log import log, reset_log
from movements import turn
from tracker import Tracker
from strategy import (get_token_from_corner, token_to_slot,
    recalulate_position, move_to_point)

# get_token_from_corner

def main():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    reset_log(robot)

    slots_x = 3 if robot.zone in [0, 3] else 5.18
    target_theta = pi/2 if robot.zone in [0, 3] else 1.5*pi
    if robot.zone in [0, 1]:
        dy = 0.9
        slot_y_0 = 2.65
    else:
        dy = -0.9
        slot_y_0 = 5.65

    while 1:
        try:
            for i in range(4):
                if i == 1:
                    get_token_from_corner(robot, robot.zone)
                elif i > 1:
                    get_token_from_corner(robot, 3 - robot.zone)

                slot_y = slot_y_0 + i*dy
                move_to_point(robot, slots_x, slot_y, target_theta)
                token_to_slot(robot)
        except:
            print_exc()
            reset_log(robot)
            print '\nRestarting in 2s...\n'
            sleep(2)


main()
