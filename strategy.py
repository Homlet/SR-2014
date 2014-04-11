from math import pi, sqrt, atan2
from time import time, sleep

from sr import INPUT_PULLUP, MARKER_ARENA

from log import push_log, pop_log, log, indented
from position import (directions_for_marker, directions_for_point,
    position_from_wall, marker_pos)
from movements import move_straight, turn, grab, put_down


# This resolution is not used everywhere on purpose
RESOLUTION = (1280, 960)

FRONT_SWITCH = 11

D = 2
SCAN_POINTS = [(D, D), (8-D, D), (8-D, 8-D), (D, 8-D)]

# We go to SLOT_POINTS when we have token.
SLOT_POINTS = [(3, 2.65), (5.18, 2.65), (5.18, 5.65), (3, 5.65)]


@indented
def token_to_slot(robot):
    """
    Assumes robot is near the slot with the token already.
    """
    markers = robot.see()
    for marker in markers:
        if marker.info.code in range(32, 40):
            line_up_to_marker(robot, marker, 0.3)
            put_down(robot)
            move_straight(robot, -0.3)
            break  # Return True?
        elif marker.info.code in range(40, 52):
            # This is unlikely to happen at the beginning
            # of the competition/match.
            pass  # Return False?
            # Check if it's in a slot.
                # If it's not our take it out?


@indented
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
        for i in xrange(3):
            means.append(sum([p[i] for p in positions]) / len(positions))
            square_mean = sum([p[i]**2 for p in positions]) / len(positions)
            if sqrt(square_mean - means[i]**2) > 0.5:  # TODO: tweak.
                log(robot, "Position data too varied.")
                return False

        log(robot, "New position: x=%.1f, y=%.1f, theta=%.1f" % means)
        robot.position.reset_to(means)
        return True
    else:
        log(robot, "No markers seen.")
        return False


def avoid_obstacles(robot):  # This will need more arguments
    markers = robot.see()
    for marker in markers:
        if marker.info.code in range(28, 32):
            markers_ = robot.see()
            for m in markers_:  # Leaves m being a robot marker
                if m.info.code in range(28, 32):
                    break
            else:
                print 'Lost opponent\'s robot'
                return
            # Works out direction of movement of that robot
            x0, y0 = marker_pos(marker, robot.position)
            x1, y1 = marker_pos(m, robot.position)
            dx = x1 - x0
            dy = y1 - y0
            if dx < 0.1 and dy < 0.1:  # 'Not moving'
                pass
                # Is it in our way?
            else:
                d_theta = (5*pi/2 - atan2(dy, dx)) % 2*pi
                theta = robot.position.theta
                # Is it going towars us?
                if ((d_theta+pi) % 2*pi) <= theta + pi/9 and \
                   ((d_theta+pi) % 2*pi) >= theta - pi/9:
                        pass
                # Is it moving out of our way or is it an obstacle?

        elif marker.info.code in range(40, 52):
            if our_token(marker, robot.zone):
                pass
                # This should happen quite often
            else:
                pass
                # Either ignore it or move around it
                # We may not need this


@indented
def move_to_point(robot, x, y, target_theta):
    """
    Given the robot's current tracked position, moves to point
    (x, y), where x and y are metres from the origin.
    """
    smart = False
    log(robot, "Moving to point x=%.1f y=%.1f...%.1f " % (x, y, target_theta))
    dist, angle = directions_for_point(robot, x, y)
    log(robot, "dist=%.1f angle=%.1f" % (dist, angle))

    turn(robot, angle)
    sleep(0.7)
    if smart:
        avoid_obstacles(robot)

    # Check area in front of us before moving.
    # If there's a robot, take a picture again, work out where it's going.
        # Take measures to avoid it, if needed.
    # If there's a token, we could either ignore it or move around it.
    # Anyway, if there are obstacles our way, we must move in steps.

    move_straight(robot, dist)

    d_theta = target_theta - robot.position.theta
    if d_theta > pi:
        d_theta -= pi+pi
    elif d_theta < -pi:
        d_theta += pi+pi
    turn(robot, d_theta)

    log(robot, "done.")


@indented
def get_token_from_corner(robot, zone):
    """
    Moves to specified corner, finds a marker and picks it up.
    """
    log(robot, "Attempting to get token from corner of zone %d..." % (zone))
    token_marker = look_for_token(robot, zone)
    if token_marker:
        line_up_to_marker(robot, token_marker)
        put_down(robot)
        move_till_touch(robot)
        grab(robot)
        return True
    else:
        log(robot, "No tokens found.")
        return False


@indented
def look_for_token(robot, zone):
    """
    Go to zone's corner and return markers seen there.
    Turns the robot so that it then scans the corner
    by turning through 90 degrees.
    """
    log(robot, "Moving to corner of zone %d..." % (zone))

    zx, zy = SCAN_POINTS[zone]
    target_theta = (1.5*pi + zone*pi/2) % (pi+pi)
    move_to_point(robot, zx, zy, target_theta)

    log(robot, "done.")

    for i in xrange(3):
        markers = robot.see(res=RESOLUTION)
        for marker in markers:
            n = marker.info.code
            if n in xrange(28):
                robot.position.reset_to(position_from_wall(marker))
            elif our_token(marker, robot.zone):
                return marker
        turn(robot)
        sleep(0.5)
    else:
        return None


@indented
def line_up_to_marker(robot, marker, dist=0.4):
    """
    Moves the robot 'dist' metres in front of a given marker.
    """
    log(robot, "Lining up to marker:")

    dist, angle1, angle2 = directions_for_marker(marker, d=dist)
    log(robot, "dist=%.2f, angle1=%.2f, angle2=%.2f" % (dist, angle1, angle2))

    turn(robot, angle1)
    sleep(0.75)
    move_straight(robot, dist)
    sleep(0.75)
    turn(robot, angle2)

    log(robot, "done.")


@indented
def move_till_touch(robot, time_limit=30):  # Experiment with limit default.
    """
    Moves the robot forward at a constant rate until a
    switch is triggered or if it has been moving for longer
    than `limit` seconds. Returns False if it didn't hit
    anything within the limit.
    """
    touching_marker = False
    beyond_time_limit = False

    log(robot, "Moving into marker...")

    start = time()
    robot.motors[0].m0.power = 40
    robot.motors[0].m1.power = 40
    while not (touching_marker or beyond_time_limit):
        touching_marker = not robot.ruggeduinos[0].digital_read(FRONT_SWITCH)
        beyond_time_limit = time() > start + time_limit
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0

    log(robot, "done.")

    # Update robot.position with distance moved.
    robot.position.move((time()-start) / 5)

    return not beyond_time_limit


def our_token(token_marker, zone):
    return token_marker.info.code in range(40 + zone, 49 + zone, 4)
