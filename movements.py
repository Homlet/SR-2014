from math import sin, cos, pi
from time import sleep

from mechanics import Journey, open_arms, close_arms, raise_arms, lower_arms, extend_arms, retract_arms
from position import position_from_zone

class Tracker():
    """
    Tracks the robot's current position and bearing.
    
    Position is stored as a vector, (x, y),
    where x and y are metres from the origin.
    
    Bearing is stored in RADIANS.
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

def prepare_for_grab(robot):
    close_arms(robot)
    lower_arms(robot)
    extend_arms(robot)
    open_arms(robot)

def grab(robot):
    close_arms(robot)
    raise_arms(robot)
    retract_arms(robot)
