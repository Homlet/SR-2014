from mechanics import (close_arms, lower_arms, extend_arms,
    retract_arms, open_arms, raise_arms, Journey)
from time import sleep

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


def grab(robot):
    close_arms(robot)
    sleep(0.4)
    raise_arms(robot)
    sleep(0.8)
    retract_arms(robot)


def put_down(robot):
    close_arms(robot)
    extend_arms(robot)
    sleep(0.1)
    lower_arms(robot)
    sleep(0.5)
    open_arms(robot)
