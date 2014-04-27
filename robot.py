from time import sleep
from traceback import print_exc
from math import pi

from sr import Robot, INPUT_PULLUP

from log import reset_log, log
from tracker import Tracker
from sound import Sound
from strategy import (get_token_from_corner, token_to_slot, move_to_point,
    move_till_touch, FRONT_SWITCH, token_to_slot_2, roll_marker)
from movements import put_down, grab, move_straight, turn
from mechanics import (ARMS_FORWARDS_STOP, ARMS_BACKWARDS_STOP,
    LEFT_MOTOR_SWITCH, RIGHT_MOTOR_SWITCH, raise_arms, lower_arms)


USING_SOUND = True


def main():
    """
    Robot will use two corners on one side of the wall in the arena.
    It will try to put all 4 tokens into slots. This gives us 9 points.
    """
    option = 2

    robot = Robot()
    reset_log(robot)
    robot.sound = Sound(robot, USING_SOUND)
    robot.sound.play('R2D2')
    robot.position = Tracker(robot.zone)
    set_pins(robot)

    slots_x = 2.91 if robot.zone in [0, 3] else 5.09
    target_theta = pi/2 if robot.zone in [0, 3] else 1.5*pi
    if robot.zone in [0, 1]:
        dy = 0.9
        slot_y_0 = 2.65
    else:
        dy = -0.9
        slot_y_0 = 5.65

    while 1:
        try:
            if option == 1:
                put_down(robot)
                grab(robot)

                token_to_slot(robot, robot.zone)
                for i in range(4):
                    zone = robot.zone if i < 2 else 3-robot.zone

                    has_token = get_token_from_corner(robot, zone)

                    if has_token:
                        token_to_slot(robot, zone)
            elif option == 2:
                put_down(robot)
                grab(robot)
                for i in range(4):
                    zone = robot.zone if i < 2 else 3-robot.zone
                    if i == 0:
                        move_to_point(robot, slots_x, slot_y_0+0.9, target_theta)
                        token_to_slot_2(robot)
                    elif i == 1:
                        move_to_point(robot, 2, 2)
                        get_token_from_corner(robot, zone)
                        move_to_point(robot, slots_x, slot_y_0, target_theta)
                        token_to_slot_2(robot)
                    else:
                        move_to_point(robot, 2, 2)
                        get_token_from_corner(robot, zone)
                        slot_y = slot_y_0 + dy*i
                        move_to_point(robot, slots_x, slot_y, target_theta)
                        token_to_slot_2(robot)
        except:
            print_exc()
            restart(robot)


def restart(robot):
    reset_log(robot)
    print "\nERROR - Restarting...\n"
    for i in range(3):
        robot.power.led[i] = 1
        sleep(0.9)
    for i in range(3):
        robot.power.led[i] = 0


def set_pins(robot):
    robot.ruggeduinos[0].pin_mode(FRONT_SWITCH, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(RIGHT_MOTOR_SWITCH, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(LEFT_MOTOR_SWITCH, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(ARMS_FORWARDS_STOP, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(ARMS_BACKWARDS_STOP, INPUT_PULLUP)


def main_test(robot):
	while True:
		robot.power.led[0] = 1
		grab(robot)
		robot.power.led[0] = 0
		sleep(2)
		robot.power.led[1] = 1
		put_down(robot)
		robot.power.led[1] = 0
		sleep(2)
        print "Cycled!"


def approx(robot):
    z = robot.zone
    angles = [pi/6, pi/3, pi/2]
    distances = [1, 0.5, 0.3, 0.1, 0.5]
    if z == 0:
        for phi in angles:
            for i in range(3):
                for j in [1, -1]:
                    print 'turning %.2f' % phi
                    turn(robot, phi*j)
                    sleep(5)
    else:
        for dist in distances:
            for i in [1, -1]:
                print 'moving %.2f' % dist*i
                move_straight(robot, dist*i)
                sleep(5)


def avoidance_test(robot):
    move_to_point(robot, 1, 1, robot.position.theta, True)


main()
