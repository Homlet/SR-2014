from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep, time

from sr import Robot, INPUT_PULLUP

from movements import move_straight, turn, Tracker
# from position import compute_directions_for
from position import *

def line_up_to(marker, robot, dist=0.4):
    dist, angle1, angle2 = compute_directions_for(marker, d=dist)
    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(1)
    move_straight(robot, dist)
    sleep(1)
    turn(robot, angle2)
    
def move_till_touch(robot):
    robot.ruggeduinos[0].pin_mode(11, INPUT_PULLUP)
    touchingMarker = lambda: robot.ruggeduinos[0].digital_read(11)
    
    robot.motors[0].m0.power = 30
    robot.motors[0].m1.power = 30
    start = time()
    print 'Moving Forwards'
    while not touchingMarker():
        pass
    print'Touching Marker'
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0
    # Update robot.position with distance moved.
    robot.position.move((time() - start) / 5)

def get_directions_for_XY(robot, x, y):
    """
    Returns angle to turn and the distance to move.
    """
    x0, y0, theta = robot.position.x, robot.position.y, robot.position.angle
    dx = x - x0
    dy = y - y0
    dist = sqrt(dx*dx + dy*dy)
    gamma = atan2(dx, dy)
    alpha = (theta + gamma)
    print 'turn:%.1f, move:%.1f' % (alpha, dist)
    print 'theta = %.1f' % (theta)
    return dist, alpha

def nick_main():
    robot = Robot()
    ourZone = robot.zone
    robot.position = Tracker(ourZone)
    d = 2.2
    significantPoints = [(d, d), (8-d, d), (8-d, 8-d), (d, 8-d)]
    dist, alpha = get_directions_for_XY(robot, *significantPoints[ourZone])
    turn(robot, alpha)
    move_straight(robot, dist)

    
# def main():
#     markersInSight = robot.see()
#     while not markersInSight:
#         turn(robot)
#         sleep(0.5)
#         markersInSight = robot.see()
#     marker = markersInSight[0]
    
#     line_up_to(marker, robot)
#     move_till_touch(robot)
    
#     print 'End Position: ', (robot.position.x, robot.position.y)
    
# robot = Robot()
# robot.position = Tracker(robot.zone)
# print 'Start position:', (robot.position.x, robot.position.y), robot.position.angle

# worldExists = True
# while worldExists:
#     main()
#     sleep(5)
nick_main()
