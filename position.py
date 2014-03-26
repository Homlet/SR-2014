from math import sin, cos, atan2, radians, pi, hypot


STARTING_DISTANCE = 0.6591


class Zone:
    def __init__(self, zoneNumber):
        #                   x1   y1   x2   y2
        zoneBoundaries = [(291, 250, 409, 400),
                          (409, 250, 509, 400),
                          (291, 400, 409, 550),
                          (409, 400, 509, 550)]
        self.number = zoneNumber
        self.tokens = []
        self.boundaries = zoneBoundaries[zoneNumber]

    def is_inside(self, x, y):
        """Tells whether x, y is inside the zone"""
        return in_range(x, self.boundaries[0], self.boundaries[2]) and \
               in_range(y, self.boundaries[1], self.boundaries[3])


def position_from_wall(marker):
    """
    Computes position of the robot on the arena with O(0, 0) being
    top left corner of the arena.
    Bearing is angle in radians from upward vertical in clock-wise direction.
    """

    n = marker.info.code
    w = n // 7
    d = n % 7 + 1
    val = [0, d, 8, 8-d, 0]
    alpha = -radians(marker.rot_y)
    beta = -radians(marker.orientation.rot_y)
    theta = beta + pi / 2 * (3-w)

    # ix and iy are marker's coordinates on the wall starting from O
    ix = val[w]
    iy = val[w+1]
    # dx and dy - where robot is relatively to wall marker
    dx = marker.dist * cos(theta - alpha)
    dy = marker.dist * sin(theta - alpha)
    return ix - dy, iy + dx, theta


def position_from_slot(marker):
    xList = [3.5, 3.68]
    yList = [2.65, 3.55, 4.45, 5.35]
    alpha = radians(marker.rot_y)
    beta = radians(marker.orientation.rot_y)
    n = marker.info.code - 32

    if (n % 4) < 2:
        theta = pi/2 - beta
    else:
        theta = 1.5*pi - beta

    dx = marker.dist * cos(theta - alpha)
    dy = marker.dist * sin(theta - alpha)

    slotX = xList[n % 2]
    if n < 4:
        slotY = yList[n % 2]
    else:
        slotY = yList[n % 2 + 2]
    return slotX - dy, slotY + dx, theta


def position_from_zone(zone_number):
    dist = STARTING_DISTANCE
    theta = ((3*pi)/4 + (pi/2 * zone_number)) % (2*pi)
    x = dist if zone_number in (0, 3) else 8 - dist
    y = dist if zone_number in (0, 1) else 8 - dist
    return x, y, theta


def compute_token_pos(tokenMarker, x, y, theta):
    alpha = radians(tokenMarker.rot_y)
    X = x + tokenMarker.dist*cos(theta - alpha)
    Y = y - tokenMarker.dist*sin(theta - alpha)
    return X, Y


def compute_directions_for_marker(marker, d=1):
    """
    The function provides neccesary information to line up for marker
    'd' metres away from it

    Returns angle 'gamma' (radians) for robot to turn
    and move 'distance' meters forward to get 1m in front of the token
    and angle to turn towards the marker when it stops moving

    This function assumes angles are positive when marker is to the left
    of the robot and is turned away from it anti-clockwise

    """
    alpha = radians(marker.rot_y)
    beta = radians(marker.orientation.rot_y)
    X = marker.dist * sin(alpha)
    Y = marker.dist * cos(alpha)
    x = X - d*sin(beta)
    y = Y - d*cos(beta)
    gamma = atan2(x, y)
    return hypot(x, y), gamma, beta - gamma


def compute_directions_for_point(robot, x, y):
    """
    Returns angle to turn and the distance to move.
    """
    dx = x - robot.position.x
    dy = y - robot.position.y
    alpha = atan2(dx, -dy)
    # alpha is bearing robot needs to have to look at the point
    theta = robot.position.theta
    if alpha < 0:
        alpha += pi+pi
    beta = alpha - theta
    # beta is angle for robot to turn clock-wise
    if beta < -pi:
        beta += pi+pi
    if beta > pi:
        beta -= pi+pi
    return hypot(dx, dy), beta


def in_range(x, l, r):
    return l <= x <= r
