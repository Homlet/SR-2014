from math import sin, cos, sqrt
from time import sleep

from geometry import Vec2
from mechanics import Journey
from position import compute_directions_for_point, position_from_zone


class Tracker(Vec2):
	"""
		Tracks the robot's current position and angle.
		
		Position is stored as a vector, (x, y),
		where x and y are metres from the origin.
		
		Angle is stored as a bearing in RADIANS.
	"""
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
    
def move_to_point(robot, x, y):
	"""
		Given the robot's current tracked position, moves to point
		(x, y), where x and y are metres from the origin.
	"""
    dist, angle = compute_directions_for_point(robot, x, y)
    turn(robot, angle)
    sleep(0.7)
    move_straight(robot, dist)
    