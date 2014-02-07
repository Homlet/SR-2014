from math import sin, cos, atan, radians, degrees, sqrt
from time import sleep

from sr import Robot

from movements import move_straight, turn
from position import compute_directions_for

def main0():
    robot = Robot()
    markersInSight = robot.see()
    while not markersInSight:
        movements.turn(robot)
        sleep(0.5)
        markersInSight = robot.see()

    marker = markersInSight[0]
    dist, angle1, angle2 = compute_directions_for(marker)
#    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (distance, angle1, angle2)

    movements.turn(robot, angle1)
    sleep(1)
    movements.move_straight(robot, dist)
    sleep(1)
    movements.turn(robot, angle2)

def main():
    robot = Robot()
    movements.move_straight(robot, 10)  # 10 meters :D

main()