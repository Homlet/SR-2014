from math import *

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
    bearing = beta + pi/2*(3-w)

    ix = val[w]
    iy = val[w+1]
    dx = marker.dist * cos(bearing - alpha)
    dy = marker.dist * sin(bearing - alpha)
    # print(ix, iy, dx, dy)
    return ix - dy, iy + dx, bearing

def compute_directions_for(marker, y=1):
    """
    New implementation that may or may not work, using cosine rule.
    
    It assumes clockwise angles are positive, but I don't know where
    the provided angles are measured from, so it may need some sign
    tweaking.
    
    If it doesn't work, we can go back to Nikita's code and work
    from there.
    
    http://i.imgur.com/YiAnxK4.jpg
    """
    alpha = radians(marker.rot_y)
    beta = radians(marker.orientation.rot_y)
    print 'alpha=%.2f, beta=%.2f' % (alpha, beta)
    
    theta = beta - alpha
    x = sqrt(y**2 + marker.dist**2 - 2*y*cos(theta))
    gamma = acos((marker.dist**2 + x**2 - y**2) / (2*marker.dist*x))
    delta = theta + alpha - gamma
    
    return x, gamma, delta
    