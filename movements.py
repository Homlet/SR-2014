from time import sleep

from mechanics import (close_arms, lower_arms, extend_arms,
    retract_arms, open_arms, raise_arms, Journey)
from logging import log, indented


def move_straight(robot, dist):
    """
    Moves the robot dist metres forward and updates the tracker.
    """
    journey = Journey(robot, distance=dist)
    journey.start()
    robot.position.move(dist)


def turn(robot, alpha=0.524):  # 0.524 rad = 30 degrees
    """
    Turns the robot alpha RADIANS and updates the tracker.
    """
    journey = Journey(robot, angle=alpha)
    journey.start()
    robot.position.turn(alpha)


@indented
def grab(robot):
    log(robot, "Closing arms...")
    close_arms(robot)
    sleep(0.4)

    log(robot, "Raising arms...")
    raise_arms(robot)
    sleep(0.8)

    log(robot, "Retracting arms...")
    retract_arms(robot)


@indented
def put_down(robot):
    log(robot, "Closing arms...")
    close_arms(robot)

    log(robot, "Extending arms...")
    extend_arms(robot)
    sleep(0.1)

    log(robot, "Lowering arms...")
    lower_arms(robot)
    sleep(0.5)

    log(robot, "Opening arms...")
    open_arms(robot)
