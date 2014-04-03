from math import pi, sqrt
from time import time, sleep

from sr import INPUT_PULLUP, MARKER_ARENA

from log import push_log, pop_log, log
from position import (directions_for_marker, directions_for_point,
    position_from_wall)
from movements import move_straight, turn, prepare_grab, grab, put_down


RESOLUTION = (1280, 960)

M_SWITCH_FRONT = 11

D = 2.6
SCAN_POINTS = [(D, D), (8-D, D), (8-D, 8-D), (D, 8-D)]
# These points are coordinate of corners of zones where we get points
ARENA_POINTS = [(3, 2.5), (5.18, 2.5), (5.18, 5.5), (3, 5.5)]


def get_token_from_corner(robot, zone):
    """
    Moves to specified corner, finds a marker and picks it up.
    """
    log(robot, "Getting marker from corner of zone %d..." % (zone))
    push_log(robot)
    markers = scan_corner(robot, zone)
    if markers:    
        line_up_to_marker(robot, markers[0])
        prepare_grab(robot)
        move_till_touch(robot)
        grab(robot)
        pop_log(robot)
        return True
    else:
        log(robot, "No tokens found.")
        pop_log(robot)
        return False


def token_to_slot(robot, zone):
    """
    Moves the robot to the specified slot, and places down the token.
    """
    log(robot, "Moving to zone %d..." % (zone))
    push_log(robot)

    zx, zy = ARENA_POINTS[zone]
    target_theta = pi/2 if zone in [0, 3] else 1.5*pi
    move_to_point(robot, zx, zy, target_theta)

    pop_log(robot)
    log(robot, "done.")

    log(robot, "Moving to slot...")
    push_log(robot)

    markers = robot.see(res=RESOLUTION)
    for marker in markers:
        if marker.info.n in range(32, 40):
            move_straight(robot, marker.dist - 0.3)
            break

    pop_log(robot)
    log(robot, "done.")
    
    log(robot, "Placing token in slot...")
    push_log(robot)
    put_down(robot)
    pop_log(robot)


def recalulate_position(robot):
    """
    Calculates the robot's position using nearby markers.
    If there are not enough markers to gain an accurate result,
    nothing is done.
    Returns true if the recalculation was successful.
    """
    log(robot, "Recalculating position...")

    markers = robot.see(res=RESOLUTION)
    if markers:
        positions = []
        for marker in markers:
            if marker.info.marker_type == MARKER_ARENA:
                positions.append(position_from_wall(marker))
        print(str(positions) + ' markers seen')
        if len(positions) < 3:  # TODO: tweak.
            log(robot, "Not enough markers seen.")
            return False

        means = []
        for i in range(3):
            means[i] = sum([p[i] for p in positions]) / len(positions)
            square_mean = sum([p[i]**2 for p in positions]) / len(positions)
            if sqrt(square_mean - means[i]**2) > 0.5:  # TODO: tweak.
                log(robot, "Position data too varied.")
                return False

        log(robot, "New position: x=%.1f, y=%.1f, theta=%.1f" % means)
        robot.position.x, \
        robot.position.y, \
        robot.position.theta = means
        return True
    else:
        log(robot, "No markers seen.")
        return False


def move_to_point(robot, x, y, target_theta):
    """
    Given the robot's current tracked position, moves to point
    (x, y), where x and y are metres from the origin.
    """
    log(robot, "Moving to point x=%.1f y=%.1f... %.1f " %(x, y, target_theta))
    
    dist, angle = directions_for_point(robot, x, y)
    log(robot, "dist=%.1f angle=%.1f" % (dist, angle))

    log(robot, "Turning...")
    push_log(robot)
    turn(robot, angle)
    pop_log(robot)
    log(robot, "done.")

    sleep(0.7)

    log(robot, "Moving forwards...")
    push_log(robot)
    move_straight(robot, dist)

    d_theta = target_theta - robot.position.theta
    if d_theta > pi:
        d_theta -= pi+pi
    elif d_theta < -pi:
        d_theta += pi+pi
    turn(robot, d_theta)

    pop_log(robot)
    log(robot, "done.")


def scan_corner(robot, zone):
    """
    Go to zone's corner and return markers seen there.
    Turns the robot so that it then scans the corner
    by turning through 90 degrees.
    
    We may want to increase that angle to account for token scattering
    """
    log(robot, "Moving to corner of zone %d..." % (zone))
    push_log(robot)

    zx, zy = SCAN_POINTS[zone]
    target_theta = (1.5*pi + zone*pi/2) % (pi+pi)
    move_to_point(robot, zx, zy, target_theta)

    pop_log(robot)
    log(robot, "done.")
    
    log(robot, "Scanning for token markers...")
    push_log(robot)
    
    markers = robot.see(res=RESOLUTION)
    for i in range(3):
        if markers: break
        turn(robot)
        sleep(1)
        markers = robot.see(res=RESOLUTION)

    pop_log(robot)
    log(robot, "done.")
    
    return markers


def scan_for_markers(robot, angle=0.524):
    """
    Rotates on the spot in increments until a marker(s) is seen.
    Then returns list of visible markers.
    Can be passed angle=0 to stare forwards.
    """
    markers_in_sight = robot.see(res=RESOLUTION)
    while not markers_in_sight:
        turn(robot, angle)
        sleep(0.5)
        markers_in_sight = robot.see(res=RESOLUTION)
    return markers_in_sight


def line_up_to_marker(robot, marker, dist=0.4):
    """
    Moves the robot 'dist' metres in front of a given marker.
    """
    log(robot, "Lining up to marker:")
    push_log(robot)

    dist, angle1, angle2 = directions_for_marker(marker, d=dist)
    log(robot, "dist=%.2f, angle1=%.2f, angle2=%.2f" % (dist, angle1, angle2))

    turn(robot, angle1)
    sleep(0.75)
    move_straight(robot, dist)
    sleep(0.75)
    turn(robot, angle2)

    pop_log(robot)
    log(robot, "done.")


def move_till_touch(robot, time_limit=30):  # Experiment with limit default.
    """
    Moves the robot forward at a constant rate until a
    switch is triggered or if it has been moving for longer
    than `limit` seconds. Returns False if it didn't hit
    anything within the limit.
    """
    robot.ruggeduinos[0].pin_mode(M_SWITCH_FRONT, INPUT_PULLUP)

    touching_marker = False
    beyond_time_limit = False

    log(robot, "Moving into marker...")

    start = time()
    robot.motors[0].m0.power = 30
    robot.motors[0].m1.power = 30
    while not (touching_marker or beyond_time_limit):
        touching_marker = not robot.ruggeduinos[0].digital_read(M_SWITCH_FRONT)
        beyond_time_limit = time() > start + time_limit
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0

    log(robot, "done.")

    # Update robot.position with distance moved.
    robot.position.move((time()-start) / 5)

    return not beyond_time_limit
