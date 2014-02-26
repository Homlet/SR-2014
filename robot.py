from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep

from sr import Robot, INPUT_PULLUP

from movements import move_straight, turn
from position import compute_directions_for

def line_up_to(marker, robot, dist=0.2):
    dist, angle1, angle2 = compute_directions_for(marker, d=0.2)
    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(1)
    move_straight(robot, dist)
    sleep(1)
    turn(robot, angle2)
    
def main():
    worldExists = True

    markersInSight = robot.see()
    while not markersInSight:
        turn(robot)
        sleep(0.5)
        markersInSight = robot.see()
    marker = markersInSight[0]
    line_up_to(marker, robot)
    touchingMarker = lambda: robot.ruggeduinos[0].digital_read( 11 )
    robot.motors[0].m0.power = 30
    robot.motors[0].m1.power = 30
    robot.ruggeduinos[0].pin_mode( 11, INPUT_PULLUP )
    while not touchingMarker():
        print "Not hit anything yet, moving forward"
    print'Touching Marker'
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0

robot = Robot()
while 1:
    main()
    sleep(10)
