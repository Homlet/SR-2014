from time import sleep, time
from traceback import print_exc
import math
from sr import Robot

from log import reset_log
from movements import Tracker, turn
from strategy import get_token_from_corner, token_to_slot


def resolution_test(robot):
    resolutions = [(1280, 960), (800, 600)]
    markers = robot.see(res=res)
    while not markers:
        for res in resolutions:
            start = time()
            markers = robot.see(res=res)
            print 'took %.1f s to take picture with %s' % (time()-start, res,)
        print 'Seen %d markers' % (len(markers))

def main():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    reset_log(robot)

    while 1:
        try:
            # get_token_from_corner(robot, robot.zone)
            # token_to_slot(robot, robot.zone)
            resolution_test(robot)
            # sleep(0)
        except:
            print_exc()
            reset_log(robot)
            print '\nRestarting in 2s...\n'
            sleep(2)


main()
