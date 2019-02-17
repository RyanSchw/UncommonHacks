import math
import random

class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    @classmethod
    def rand(self):
        return Vec2d(random.random(), random.random())

    def dist(self, other):
        return (self - other).mag()

    def mag(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def unit(self):
        mag = self.mag()
        if mag == 0:
            return Vec2d(0,0)
        return Vec2d(self.x / mag,  self.y/ mag)

    # Element by element multiplication
    def elm_mult(self, other):
        return Vec2d(self.x * other.x, self.y * other.y)
    # Element by element division
    def elm_div(self, other):
        return Vec2d(self.x / other.x, self.y / other.y)

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Vec2d(self.x * scalar, self.y * scalar)
    def __truediv__(self, scalar):
        assert scalar != 0
        return Vec2d(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.mag() > other.mag() and self != other

def create_vec2d_array(x_vec, y_vec):
    assert len(x_vec) == len(y_vec), "Lists not same length"

    points = []
    for (x, y) in zip(x_vec, y_vec):
        points.append(Vec2d(x, y))

    return points