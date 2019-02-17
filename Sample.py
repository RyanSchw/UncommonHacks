import random
import Vec2d
import json

## SAMPLE CLASS
# Contains data for an timestamped position, velocity, and acceleration.
# Multiple samples create an enrire run or path that the vehicle has taken
class Sample:

    SAMPLE_ATTRIBUTES = ('pos', 'vel', 'acc', 'time')

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

    def __iter__(self):
        yield '10'

    @classmethod
    def rand(self):
        return Sample(Vec2d.rand(), Vec2d.rand(), Vec2d.rand(), random.random())

    def serialize(self):
        return '''{{
    {pos},
    {vel},
    {acc},
    "time": {time}
}}'''.format(
    pos=self.pos.serialize('pos'),
    vel=self.vel.serialize('vel'),
    acc=self.acc.serialize('acc'),
    time=self.time
)
    def serialize_array(arr):
        obj = '''{
            "samples": ['''

        for serial in arr:
            obj = obj + serial.serialize()
            if arr.index(serial) != len(arr) - 1:
                obj = obj + ', \n'

        return obj + ']}'