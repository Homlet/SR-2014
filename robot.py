from time import sleep
from traceback import print_exc
from math import degrees, pi

from sr import Robot

from movements import Tracker, turn, move_straight, prepare_for_grab, grab
from strategy import (line_up_to_marker, scan_corner, move_till_touch,
    move_to_point)
from mechanics import raise_arms, lower_arms, open_arms, close_arms

def use_arms(robot):
    while True:
        sleep(2)
        print('raise')
        raise_arms(robot)
        sleep(2)
        print('lower')
        lower_arms(robot)
        sleep(2)
        print('open')
        open_arms(robot)
        sleep(2)
        print('close')
        close_arms(robot)
        print "cycled"

def get_to_marker(robot):
    marker = scan_corner(robot, robot.zone)[0]
    line_up_to_marker(robot, marker)
    move_till_touch(robot)

def see_marker(robot):
    markers = robot.see()
    while not markers:
        markers = robot.see()
    return markers[0]

def measure_distance(robot, dist):
    marker = see_marker(robot)
    dist0 = marker.dist
    move_straight(robot, dist)
    marker = see_marker(robot)
    dist1 = marker.dist
    print 'Attempted moving %.2f m;\nMoved %.2f m' % (dist, dist0 - dist1)

def measure_angle(robot, angle):
    marker = see_marker(robot)
    alpha = marker.orientation.rot_y
    turn(robot, angle)
    sleep(1)
    marker = see_marker(robot)
    beta = marker.orientation.rot_y
    angle = degrees(angle)
    print 'Attempted turning %.1f deg;\nTurned %.1f deg' % (angle, alpha - beta)
    
    
def approximations(robot):
    distances = [0.25, 0.15, 0.1, 0.05, 0.05]
    angles = [pi/6, pi/6, pi/6, pi/12, pi/36]
    # for dist in distances:
    #     measure_distance(robot, dist)
    #     sleep(10)

    # sleep(20)

    for angle in angles:
        measure_angle(robot, angle)
        sleep(10)

def main():
    robot = Robot()
    robot.position = Tracker(robot.zone)
    while 1:
        try:
            get_to_marker(robot)
            use_arms(robot)
            # approximations(robot)
        except:
            print_exc()
            print '\nRestarting in 2s...\n'
            sleep(2)

main()
