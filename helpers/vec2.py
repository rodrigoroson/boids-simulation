import math

class Vec2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def copy(self):
        return Vec2D(self.x, self.y)

    def __add__(self, v): return Vec2D(self.x + v.x, self.y + v.y)
    def __sub__(self, v): return Vec2D(self.x - v.x, self.y - v.y)
    def __mul__(self, a): return Vec2D(self.x * a, self.y * a)
    def __truediv__(self, a): 
        if a == 0: return Vec2D(0,0)
        return Vec2D(self.x / a, self.y / a)
    
    def mod(self): return math.hypot(self.x, self.y)
    
    def normalize(self):
        m = self.mod()
        if m == 0: return Vec2D(0,0)
        return self / m
    
    def safe_normalize(self):
        return self.normalize() if self.mod() > 1e-6 else Vec2D(0,0)

    def limit(self, max_val):
        m = self.mod()
        if m > max_val:
            return self.normalize() * max_val
        return self

    def tuple(self): return (self.x, self.y)

    def angle_to(self, other) -> float:
        # returns angle in radians between self and other
        dot = self.x * other.x + self.y * other.y
        m1 = self.mod()
        m2 = other.mod()
        if m1 == 0 or m2 == 0: return 0.0
        cosv = max(-1.0, min(1.0, dot / (m1 * m2)))
        return math.acos(cosv)