from time import sleep
from traceback import print_exc
from math import pi

from sr import Robot, INPUT_PULLUP

from log import reset_log, log
from tracker import Tracker
from strategy import (get_token_from_corner, token_to_slot, move_to_point,
    move_till_touch, FRONT_SWITCH)
from movements import put_down, grab, move_straight, turn
from mechanics import (ARMS_FORWARDS_STOP, ARMS_BACKWARDS_STOP,
    LEFT_MOTOR_SWITCH, RIGHT_MOTOR_SWITCH, raise_arms, lower_arms)


def main():
    """
    Robot will use two corners on one side of the wall in the arena.
    It will try to put all 4 tokens into slots. This gives us 9 points.
    """
    robot = Robot()
    robot.position = Tracker(robot.zone)
    set_pins(robot)
    reset_log(robot)

    while 1:
        try:
            log(robot, "Setting arms to default position...")
            grab(robot)
            
            log(robot, "Moving starting token to slot.")
            token_to_slot(robot, robot.zone)

            for i in range(4):
                zone = robot.zone if i < 2 else 3-robot.zone
                
                log(robot, "Taking token from corner %d" % (zone))
                has_token = get_token_from_corner(robot, zone)
                
                if has_token:
                    log(robot, "Taking token to slot.")
                    token_to_slot(robot, zone)
        except:
            print_exc()
            reset_log(robot)
            print '\nRestarting in 2s...\n'
            sleep(2)


def main_test():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    set_pins(robot)
    reset_log(robot)
    while 1:
        log(robot, "Putting down arms...")
        put_down(robot)
        move_straight(robot, -0.5)
        log(robot, "done.")
        sleep(1)
        move_till_touch(robot)
        log(robot, "Grabbing token...")
        grab(robot)
        move_straight(robot, 1.5)
        turn(robot, pi/2)
        log(robot, "done.")
        sleep(5)


def set_pins(robot):
    robot.ruggeduinos[0].pin_mode(FRONT_SWITCH, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(RIGHT_MOTOR_SWITCH, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(LEFT_MOTOR_SWITCH, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(ARMS_FORWARDS_STOP, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(ARMS_BACKWARDS_STOP, INPUT_PULLUP)


main()
