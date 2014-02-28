from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep, time

from sr import Robot, INPUT_PULLUP

from movements import move_straight, turn
# from position import compute_directions_for, Tracker
from position import *

def line_up_to(marker, robot, dist=0.4):
    dist, angle1, angle2 = compute_directions_for(marker, d=dist)
    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(1)
    move_straight(robot, dist)
    sleep(1)
    turn(robot, angle2)
    return dist, angle1, angle2
    
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
    # Returns distance moved
    return (time() - start) / 5
    
def main0():
    
    tracker = Tracker(0, 0, 0)

    markersInSight = robot.see()
    while not markersInSight:
        turn(robot)
        sleep(0.5)
        markersInSight = robot.see()
    marker = markersInSight[0]
    
    dist1, angle1, angle2 = line_up_to(marker, robot)
    dist2 = move_till_touch(robot)
    
    tracker.move(angle1, dist1)
    tracker.move(angle2, dist2)
    
    print tracker.x, tracker.y

def main():
    markers = robot.see()
    if markers:
        m = markers[0]
    else:
        return
    n = m.info.code
    if n == 36:
        print position_from_slot(m)
    else:
        print compute_position(m)
    
robot = Robot()
worldExists = True
while worldExists:
    main()
    sleep(5)
