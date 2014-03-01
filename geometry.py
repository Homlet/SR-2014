from math import sqrt


class Vec2:
    """
    2D vector for easier storage and manipulation of positions.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vec2(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other):
        return Vec2(self.x-other.x, self.y-other.y)
        
    def __mul__(self, scalar):
        return Vec2(self.x*scalar, self.y*scalar)
        
    def __neg__(self):
        return Vec2(-self.x, -self.y)
    
    def len(self):
        return sqrt(self.x**2 + self.y**2)
    
    def dist(self, other):
        return sqrt((other.x-self.x)**2 + (other.y-self.y)**2)
