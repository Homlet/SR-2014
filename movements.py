from mechanics import Journey
from position import position_from_zone
from math import sin, cos

def move_straight(robot, dist):
    journey = Journey(robot, distance=dist)
    journey.start()
    robot.position.move(dist)

def turn(robot, alpha=0.524):  # 0.524 rad = 30 degrees
    journey = Journey(robot, angle=alpha)
    journey.start()
    robot.position.angle += alpha

class Tracker:
    def __init__(self, zone_number):
        x, y, angle = position_from_zone(zone_number)
        self.reset(x, y, angle)
    
    def move(self, dist):
        self.x += dist * sin(self.angle)
        self.y += dist * cos(self.angle)
        
    def reset(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
