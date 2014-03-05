from math import sin, cos, pi
from time import sleep

from mechanics import Journey

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
        print 'Moving:', dist, self.theta
        print '    Position before:', (self.x, self.y)
        self.x += dist * sin(self.theta)
        self.y -= dist * cos(self.theta)
        print '    Position after:', (self.x, self.y)
    
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
