from mechanics import Journey
from position import position_from_zone
from math import sin, cos, sqrt


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vec2(self.x+other.x, self.y+other.y)
    
    def dist(self, other):
        return sqrt((other.x-self.x)**2 + (other.y-self.y)**2)

class Tracker(Vec2):
    def __init__(self, zone_number):
        position = position_from_zone(zone_number)
        self.x, self.y, self.angle = position
    
    def move(self, dist):
        print 'Moving tracker:', dist, self.angle
        print '    Before position:', (self.x, self.y)
        self.x += dist * sin(self.angle)
        self.y -= dist * cos(self.angle)
        print '    After position:', (self.x, self.y)
    
    def turn(self, angle):
        self.angle += angle


def move_straight(robot, dist):
    journey = Journey(robot, distance=dist)
    journey.start()
    robot.position.move(dist)

def turn(robot, alpha=0.524):  # 0.524 rad = 30 degrees
    journey = Journey(robot, angle=alpha)
    journey.start()
    robot.position.turn(alpha)
    
def move_to_point(robot, x, y):
    pass
    