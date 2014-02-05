from sr import *

import movements
from math import sin, cos, atan, radians, degrees, sqrt
from time import sleep

def compute_directions(marker, d=1):
    """
    The function provides neccesary information to line up for marker
    'd' metres away from it

    Returns angle 'gamma'(radians) for robot to turn
    and move 'distance'meters forward to get 1m in front of the token
    and angle to turn towards the marker when it stops moving

    This function assumes angles are positive when marker is to the left
    of the robot and is turned away from it anti-clockwise

    """
    alpha = radians(marker.rot_y)
    beta = radians(marker.orientation.rot_y)
    X = marker.dist * sin(alpha)
    Y = marker.dist * cos(alpha)
    x = X - d*sin(beta)
    y = Y - d*cos(beta)
    gamma = atan(x / y)
    distance = sqrt(x*x+ y*y)
    print 'distance=%.2f, alpha=%.2f, beta=%.2f' % (distance, degrees(alpha), degrees(beta))
    return distance, gamma, alpha - gamma

def main():
    robot = Robot()
    markersInSight = robot.see()
    while not markersInSight:
        movements.turn(robot)
        sleep(0.5)
        markersInSight = robot.see()

    marker = markersInSight[0]
    distance, angle1, angle2 = compute_directions(marker)
#    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (distance, angle1, angle2)

    movements.turn(robot, angle1)
    sleep(1)
    movements.move_straight(robot, distance)
    sleep(1)
    movements.turn(robot, angle2)
    movements.move_straight(robot, robot.see()[0].dist)

main()