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

    
def print_file(path):
    with open(path) as file:
        for l in file: print(l, end="")


def main():
    """
    Robot will use two corners on one side of the wall in the arena.
    It will try to put all 4 tokens into slots. This gives us 9 points.
    """
    robot = Robot()
    robot.position = Tracker(robot.zone)
    set_pins(robot)
    reset_log(robot)
    
    # GO TEAM COLLYERS!
    print_file("header.txt")

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
            log(robot, "Setting arms to default position...")
            grab(robot)
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
