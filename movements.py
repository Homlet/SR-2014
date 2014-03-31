from math import sin, cos, pi
from time import sleep

from mechanics import (init_arms_pins, close_arms, lower_arms, extend_arms,
    open_arms, raise_arms, Journey)
from position import position_from_zone


ARMS_POWER = 15


class Tracker():
    """
    Tracks the robot's current position and bearing.
    Position is stored as displacement from corner 0: x, y in meters.
    Bearing is stored as theta in radians.
    """
    def __init__(self, zoneNumber):
        self.x, self.y, self.theta = position_from_zone(zoneNumber)

    def move(self, dist):
        self.x += dist * sin(self.theta)
        self.y -= dist * cos(self.theta)

    def turn(self, angle):
        self.theta += angle
        self.theta %= 2*pi


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


def prepare_grab(robot):
    init_arms_pins(robot)
    close_arms(robot)
    lower_arms(robot)
    extend_arms(robot, ARMS_POWER)
    open_arms(robot)


def grab(robot):
    init_arms_pins(robot)
    close_arms(robot)
    raise_arms(robot)
    extend_arms(robot, -ARMS_POWER)

def put_down(robot):
    pass