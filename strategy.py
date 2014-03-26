from time import time, sleep

from sr import INPUT_PULLUP

from position import *
from movements import move_straight, turn, prepare_grab, grab


M_SWITCH_FRONT = 11

D = 2.6
SCAN_POINTS = [(D, D), (8-D, D), (8-D, 8-D), (D, 8-D)]


def get_marker_from_corner(robot, zone):
    """
    Moves to specified corner, finds a marker and picks it up.
    """
    marker = scan_corner(robot, zone)[0]
    line_up_to_marker(robot, marker)
    prepare_grab(robot)
    move_till_touch(robot)
    grab(robot)


def move_to_point(robot, x, y):
    """
    Given the robot's current tracked position, moves to point
    (x, y), where x and y are metres from the origin.
    """
    print "Moving to point x=%.1f y=%.1f ..." % (x, y)
    dist, angle = compute_directions_for_point(robot, x, y)
    print "    dist=%.1f angle=%.1f" % (dist, angle)
    print "    Turning..."
    turn(robot, angle)
    sleep(0.7)
    print "    Moving forwards...\n"
    move_straight(robot, dist)


def scan_corner(robot, zone):
    """
    Go to zone's corner and return markers seen there.
    """
    zx, zy = SCAN_POINTS[zone]
    
    print "Moving to scan zone %d" % (zone)
    move_to_point(robot, zx, zy)
    print "    done."
    
    print 'Scanning corner for markers...'
    return whats_around(robot)


def whats_around(robot, angle=0.524):
    # Can be given angle=0 to just stare in front

    markers_in_sight = robot.see()
    while not markers_in_sight:
        turn(robot, angle)
        sleep(0.5)
        markers_in_sight = robot.see()
    return markers_in_sight


def line_up_to_marker(robot, marker, dist=0.4):
    """
    Moves the robot 'dist' metres in front of a given marker.
    """
    print 'Lining up to marker:'
    dist, angle1, angle2 = compute_directions_for_marker(marker, d=dist)
    print '    dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(0.75)
    move_straight(robot, dist)
    sleep(0.75)
    turn(robot, angle2)


def move_till_touch(robot, time_limit=30): # TODO: Experiment with limit default
    """
    Moves the robot forward at a constant rate until a
    switch is triggered or if it has been moving for longer
    than `limit` seconds. Returns False if it didn't hit
    anything within the limit.
    """
    robot.ruggeduinos[0].pin_mode(M_SWITCH_FRONT, INPUT_PULLUP)
        
    touching_marker = False
    beyond_time_limit = False
    
    print 'Moving into marker...'
    start = time()
    robot.motors[0].m0.power = 30
    robot.motors[0].m1.power = 30
    while not (touching_marker or beyond_time_limit):
        touching_marker = robot.ruggeduinos[0].digital_read(M_SWITCH_FRONT)
        beyond_time_limit = time() > start + time_limit
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0
    print '    marker touched.'
    
    # Update robot.position with distance moved.
    robot.position.move((time() - start) / 5)
    
    return not beyond_time_limit
