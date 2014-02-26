from math import sin, cos, atan2, radians, sqrt, pi

class Zone:
    def __init__(self, zoneNumber):
        #                   x1  y1    x2   y2
        zoneBoundaries = [(291, 250, 409, 400),
                          (409, 250, 509, 400),
                          (291, 400, 409, 550),
                          (409, 400, 509, 550)]
        self.number = zoneNumber
        self.tokens = []
        self.boundaries = zoneBoundaries[zoneNumber]

    def is_inside(self, token, x, y):
        """ Tells whether token is inside the zone"""
        return in_range(x, self.boundaries[0], self.boundaries[2]) and \
               in_range(y, self.boundaries[1], self.boundaries[3])

def in_range(x, l, r):
    return l <= x <= r

def compute_token_pos(tokenMarker, x, y, o):
    alpha = radians(tokenMarker.rot_y)
    X = x + tokenMarker.dist*cos(o - alpha)
    Y = y - tokenMarker.dist*sin(o - alpha)
    return X, Y

def compute_position(marker):
    n = marker.info.code
    w = n // 7
    d = n%7 + 1
    val = [0, d, 8, 8-d, 0]
    alpha = -radians(marker.rot_y)
    beta = -radians(marker.orientation.rot_y)
    bearing = beta + pi / 2 * (3-w)

    ix = val[w]
    iy = val[w+1]
    dx = marker.dist * cos(bearing - alpha)
    dy = marker.dist * sin(bearing - alpha)
    # print(ix, iy, dx, dy)
    return ix - dy, iy + dx, bearing

def compute_directions_for(marker, d=0.2):
    """
    The function provides neccesary information to line up for marker
    'd' metres away from it

    Returns angle 'gamma'(radians) for robot to turn
    and move 'distance'meters forward to get 1m in front of the token
    and angle to turn towards the marker when it stops moving

    This function assumes angles are positive when marker is to the left
    of the robot and is turned away from it anti-clockwise

    """
    alpha = radians(marker.rot_y)
    beta = radians(marker.orientation.rot_y)
    print 'alpha=%.2f, beta=%.2f' % (alpha, beta)
    X = marker.dist * sin(alpha)
    Y = marker.dist * cos(alpha)
    x = X - d*sin(beta)
    y = Y - d*cos(beta)
    gamma = atan2(x, y)
    distance = sqrt(x*x + y*y)
    return distance, gamma, beta - gamma
    

class Tracker:
    def __init__(self, x, y, angle):
        self.reset(x, y, angle)
    
    def move(self, angle, dist):
        self.angle += angle
        
        self.x += dist * sin(angle)
        self.y += dist * cos(angle)
        
    def reset(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        