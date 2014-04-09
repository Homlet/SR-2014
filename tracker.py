from math import sin, cos, pi
from position import position_from_zone


class Tracker():
    """
    Tracks the robot's current position and bearing.
    Position is stored as displacement from corner 0: x, y in meters.
    Bearing is stored as theta in radians.
    """
    def __init__(self, zoneNumber):
        self.x, self.y, self.theta = position_from_zone(zoneNumber)
        
    def __repr__(self):
        return 'Tracker(' + ', '.join([repr(self.x), repr(self.y), repr(self.theta)]) + ')'

    def move(self, dist):
        self.x += dist * sin(self.theta)
        self.y -= dist * cos(self.theta)

    def turn(self, angle):
        self.theta += angle
        self.theta %= 2*pi

    def reset_to(self, data):
        self.x, self.y, self.theta = data
