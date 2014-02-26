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
    while worldExists:
        markersInSight = robot.see()
        while not markersInSight:
            turn(robot)
            sleep(0.5)
            markersInSight = robot.see()

        line_up_to(markersInSight[0], robot)
        sleep(5)

def turning_test():
    robot = Robot()
    testNumber = 1
    if testNumber == 0:
        angles = [pi/2, pi/2, pi/4, pi/4]
        for a in angles:
            turn(robot, a)
            sleep(5)
    else:
        markersInSight = robot.see()
        while not markersInSight:
            markersInSight = robot.see()
        angles = [pi/6, pi/4]
        for a in angles:
            for i in range(2):
                angle0 = markersInSight[0].orientation.rot_y
                turn(robot, a)
                sleep(1)
                try:
                    print 'Turned %.1f radians, tried to turn %.1f radians'\
                        % (robot.see()[0].orientation.rot_y - angle0, a)
                except:
                    print 'Marker lost'
                sleep(10)

# main()
turning_test()