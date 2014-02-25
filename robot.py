from math import sin, cos, atan, radians, degrees, sqrt, pi, copysign
from time import sleep

from sr import Robot

from movements import move_straight, turn
from position import compute_directions_for

res = (1280, 720)


def line_up_to(marker, robot):
    dist, angle1, angle2 = compute_directions_for(marker)
    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(1)
    move_straight(robot, dist)
    sleep(1)
    turn(robot, angle2)
    
def main():
    world_exists = True
    robot = Robot()

    markers = robot.see(res=res)
    while world_exists:
        markers = robot.see()
        while not markers:
            turn(robot)
            sleep(0.5)
            markers = robot.see()
        line_up_to(markers[0], robot)
        
        touchingMarker = lambda: robot.ruggeduinos[0].digital_read( 11 )
        robot.motors[0].m0.power = 30
        robot.motors[0].m1.power = 30
        robot.ruggeduinos[0].pin_mode( 11, INPUT_PULLUP )
        while not touchingMarker():
            print "Not hit anything yet, moving forward"
        print'Touching Marker'
        robot.motors[0].m0.power = 0
        robot.motors[0].m1.power = 0
        
        sleep(5)

main()
