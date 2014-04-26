from math import pi, sqrt, atan2, hypot
from time import time, sleep

from sr import INPUT_PULLUP, MARKER_ARENA

from log import push_log, pop_log, log, indented
from position import (directions_for_marker, directions_for_point,
    position_from_wall, marker_pos)
from movements import move_straight, turn, grab, put_down


RESOLUTION = (1280, 960)

FRONT_SWITCH = 11

SCAN_POINTS = [(2, 2), (6, 2), (6, 6), (2, 6)]
SLOT_POINTS = [(2.91, 3.1), (5.09, 3.1), (5.09, 4.9), (2.91, 4.9)]

CRAWL_POWER = 40

@indented
def token_to_slot(robot, slot):
    """
    Moves robot near the slot, and places token on shelf.
    """
    log(robot, "Moving to zone start point...")
    slot_x = SLOT_POINTS[slot][0]
    slot_y = SLOT_POINTS[slot][1]
    slot_theta = 3 * pi/2 if slot in [1, 2] else pi/2
    move_to_point(robot, slot_x, slot_y, slot_theta)

    log(robot, "Scanning for slot markers...")
    robot.sound.play('Radar')
    markers = robot.see(res=RESOLUTION)
    found_Marker = False
    for marker in markers:
        if marker.info.code in range(32, 40):
            log(robot, "Found Token Marker:" + str(marker.info.code))
            found_Marker = True
            robot.sound.stop()
            line_up_to_marker(robot, marker, 0.4)
            sleep(0.2)
            put_down(robot)
            sleep(0.4)
            break
    if not found_Marker:
        robot.sound.stop()
        log(robot, "Marker Not Detected.")
        move_straight(robot, 0.4)
        put_down(robot)
        sleep(0.4)
    log(robot, "Moving away from marker.")
    move_straight(robot, -0.5)
    grab(robot)


@indented
def token_to_slot_2(robot):
    """
    Assumes robot is near the slot with the token already.
    """

    markers = robot.see()
    for marker in markers:
        if marker.info.code in range(32, 40):
            line_up_to_marker(robot, marker, 0.3)
            sleep(0.2)
            put_down(robot)
            sleep(0.4)
            move_straight(robot, -0.3)
            break  # Return True?
        elif marker.info.code in range(40, 52):
            # This is unlikely to happen at the beginning
            # of the competition/match.
            pass  # Return False?
            # Check if it's in a slot.
                # If it's not our take it out?


@indented
def avoid_obstacles(robot, x, y, theta):  # This will need more arguments
    markers = robot.see()
    for marker in markers:
        if marker.info.code in range(28, 32):
            markers_ = robot.see()
            for m in markers_:  # Leaves m being a robot marker
                if m.info.code in range(28, 32):
                    break
            else:
                log(robot, 'Lost opponent\'s robot')
                return
            # Works out direction of movement of that robot
            x0, y0 = marker_pos(marker, robot.position)
            x1, y1 = marker_pos(m, robot.position)
            dx = x1 - x0
            dy = y1 - y0
            DX = marker.centre.world.x - m.centre.world.x
            X = robot.position.x
            Y = robot.position.y
            dist_to_target = hypot(x-X, y-Y)
            if dx < 0.1 and dy < 0.1:  # The robot is still
                if m.dist <= dist_to_target:  # It's too close
                    log(robot, 'Robot still, too close.')
                    # Turn 45 deg away from opp.
                    log(robot, m.rot_y-pi/4)
                    turn(robot, m.rot_y-pi/4)  # TO-DO: Turn towards the centre
                    # Maybe check whether we can go to this point
                    # Find the point to go to get past the opp.
                    move_straight(robot, .2)
                    # move_straight(robot, hypot(0.5, m.dist))  # Use move_to_p.
                    # This gets us where we wanted
                    # move_to_point(robot, x, y, theta, False)
                    return True
                else:
                    return False
            else:
                opp_theta = (5*pi/2 - atan2(dy, dx)) % 2*pi
                theta = robot.position.theta
                # Is it going towars us?
                if theta - pi/9 <= ((opp_theta+pi) % (2*pi)) <= theta + pi/9:
                    # Move in parallel
                    turn(robot, opp_theta+pi-theta)  #may result in head-on co.
                    if m.dist <= dist_to_target:
                        move_straight(robot, m.centre.world.y)  # How long?
                        return True
                    else:
                        return False  # May cause trouble
                        # Get to target point
                elif hypot(X-x1, Y-y1) <= dist_to_target:  # It's too close
                    if m.centre.world.x >= 0.4:  # How close we'll get to it
                                          # if we move forwards
                        move_straight(robot, m.dist)  # How long?
                        # This gets us where we wanted
                        move_to_point(robot, x, y, theta, False)
                        return True
                    else:  # Let it pass
                        camera_delay = 1.5
                        d_left = 0.4 - m.centre.world.x
                        t_left = d_left / (DX/camera_delay)
                        if t_left < 5:  # Don't wait too long
                            sleep(t_left)
                        return False
                    return True
                else:
                    return False

        elif marker.info.code in range(40, 52):
            return False
            if our_token(marker, robot.zone):
                pass
                # This should happen quite often
            else:
                pass
                # Do something?
    else:
        log(robot, 'Seen nothing')

@indented
def move_to_point(robot, x, y, target_theta, smart=True):
    """
    Given the robot's current tracked position, moves to point
    (x, y), where x and y are metres from the origin.
    """
    log(robot, "Moving to point x=%.1f y=%.1f...%.1f " % (x, y, target_theta))
    dist, angle = directions_for_point(robot, x, y)
    robot.sound.play('Valkyries')
    log(robot, "dist=%.1f angle=%.1f" % (dist, angle))

    turn(robot, angle)
    sleep(0.1)
    if smart and not avoid_obstacles(robot, x, y, target_theta):
        move_straight(robot, dist)

    d_theta = target_theta - robot.position.theta
    print ' ! %.2f ' % d_theta
    if d_theta > pi:
        d_theta -= pi+pi
    elif d_theta < -pi:
        d_theta += pi+pi
    print(d_theta)
    turn(robot, d_theta)

    log(robot, "done.")
    robot.sound.stop()


@indented
def get_token_from_corner(robot, zone):
    """
    Moves to specified corner, finds a marker and picks it up.
    """
    log(robot, "Attempting to get token from corner of zone %d..." % (zone))
    token_marker = look_for_token(robot, zone)
    if token_marker:
        line_up_to_marker(robot, token_marker)
        robot.sound.play('Heart')
        put_down(robot)
        move_till_touch(robot)
        grab(robot)
        robot.sound.stop()
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

    log(robot, "Moved to corner of zone " + str(zone) + ".")
    robot.sound.play('Radar')
    for i in xrange(3):
        markers = robot.see(res=RESOLUTION)
        for marker in markers:
            n = marker.info.code
            if n in xrange(28):
                robot.position.reset_to(position_from_wall(marker))
            elif our_token(marker, robot.zone):
                robot.sound.stop()
                return marker
        turn(robot)
        sleep(0.2)
    else:
        robot.sound.stop()
        return None


@indented
def line_up_to_marker(robot, marker, dist=0.4):
    """
    Moves the robot 'dist' metres in front of a given marker.
    """
    log(robot, "Lining up to marker:")
    robot.sound.play('Valkyries')
    dist, angle1, angle2 = directions_for_marker(marker, d=dist)
    log(robot, "dist=%.2f, angle1=%.2f, angle2=%.2f" % (dist, angle1, angle2))

    turn(robot, angle1)
    sleep(0.3)
    move_straight(robot, dist)
    sleep(0.3)
    turn(robot, angle2)

    log(robot, "Lined up to Marker.")
    robot.sound.stop()


@indented
def move_till_touch(robot, time_limit=10):  # Experiment with limit default.
    """
    Moves the robot forward at a constant rate until a
    switch is triggered or if it has been moving for longer
    than `limit` seconds. Returns False if it didn't hit
    anything within the limit.
    """
    touching_marker = False
    beyond_time_limit = False

    log(robot, "Moving into marker...")
    robot.sound.play('DialUp')

    start = time()
    robot.motors[0].m0.power = CRAWL_POWER
    robot.motors[0].m1.power = CRAWL_POWER
    while not (touching_marker or beyond_time_limit):
        touching_marker = not robot.ruggeduinos[0].digital_read(FRONT_SWITCH)
        beyond_time_limit = time() > start + time_limit
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0

    log(robot, "Hit Marker.")

    # Update robot.position with distance moved.
    robot.position.move((time()-start) / 5)
    robot.sound.stop()
    return not beyond_time_limit


def our_token(token_marker, zone):
    return token_marker.info.code in range(40 + zone, 49 + zone, 4)
