class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vec2(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other):
        return Vec2(self.x-other.x, self.y-other.y)
    
    def __len__(self):
        return sqrt(self.x**2 + self.y**2)
    
    def dist(self, other):
        return sqrt((other.x-self.x)**2 + (other.y-self.y)**2)