import random
import math

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




SAMPLE_ATTRIBUTES = ('pos', 'vel', 'acc', 'time')

class Sample:
    def __init__(self, pos, vel, acc, time):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.time = time

    def __repr__(self):
        return 'Sample{{ pos{0}, vel{1}, acc{2}, time({3}) }}' \
            .format(self.pos.__repr__(), \
            self.vel.__repr__(), \
            self.acc.__repr__(), \
            self.time)

    @classmethod
    def rand(self):
        return Sample(Vec2d.rand(), Vec2d.rand(), Vec2d.rand(), random.random())

def create_vec2d_array(x_vec, y_vec):
    assert len(x_vec) == len(y_vec), "Lists not same length"

    points = []
    for (x, y) in zip(x_vec, y_vec):
        points.append(Vec2d(x, y))

    return points

if __name__ == '__main__':
    p = Vec2d(0, 1)
    v = Vec2d(2, 3)
    a = Vec2d(4, 5)
    t = 0.5

    s = Sample(p, v, a, t)
    print(s)

    print(Sample.rand())
