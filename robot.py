from time import sleep
from traceback import print_exc
from sr import Robot

from log import log, reset_log
from movements import Tracker, turn
from strategy import get_token_from_corner, token_to_slot, recalulate_position

def main():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    reset_log(robot)
    
    while True:
        recalulate_position(robot)
        print(robot.position)
        sleep(5)

    # while 1:
    #     try:
    #         token_to_slot(robot, robot.zone)
    #         i = 0
    #         while i < 4:
    #             zone = (robot.zone + i) % 4
    #             if get_token_from_corner(robot, zone):
    #                 token_to_slot(robot, zone)
    #             i += 1
    #     except:
    #         print_exc()
    #         reset_log(robot)
    #         print '\nRestarting in 2s...\n'
    #         sleep(2)


main()
