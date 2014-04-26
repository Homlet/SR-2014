from time import sleep

from mechanics import (close_arms, lower_arms, extend_arms,
    retract_arms, open_arms, raise_arms, Journey)
from log import log, indented


@indented
def move_straight(robot, dist):
    """
    Moves the robot dist metres forward and updates the tracker.
    """
    journey = Journey(robot, distance=dist)
    journey.start()
    robot.position.move(dist)


@indented
def turn(robot, alpha=0.524):  # 0.524 rad = 30 degrees
    """
    Turns the robot alpha RADIANS and updates the tracker.
    """

    journey = Journey(robot, angle=alpha)
    journey.start()
    robot.position.turn(alpha)


@indented
def grab(robot):
    """
    Picks up the token infront of the robot, and pulls it inside
    """
    log(robot, "Picking Up Token.")
    close_arms(robot)
    sleep(0.2)

    raise_arms(robot)
    sleep(0.4)

    retract_arms(robot)


@indented
def put_down(robot):
    """
    Places the stored token infront of the robot
    """
    log(robot, "Putting Down Token.")
    close_arms(robot)

    extend_arms(robot)
    sleep(0.1)

    lower_arms(robot)
    sleep(0.3)

    open_arms(robot)
    sleep(0.2)
