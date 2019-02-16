class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

def create_point_array(x_vec, y_vec):
    assert len(x_vec) == len(y_vec), "Lists not same length"

    points = []
    for (x, y) in zip(x_vec, y_vec):
        points.append(Point(x, y))

    return points
