from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep

from sr import Robot

from movements import move_straight, turn
from position import compute_directions_for

def line_up_to(marker, robot):
    dist, angle1, angle2 = compute_directions_for(marker)
    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(1)
    move_straight(robot, dist)
    sleep(1)
    turn(robot, angle2)
    
def main():
    worldExists = True
    robot = Robot()
    markersInSight = robot.see()
    while not markersInSight:
        # turn(robot)
        # sleep(0.5)
        markersInSight = robot.see()
    marker = markersInSight[0]
    angle = marker.orientation.rot_y
    turn(robot, angle)
    # line_up_to(markersInSight[0], robot)

while 1:
    main()
    sleep(10)
