import unittest
import sys
sys.path.append("..")

from Sample import Sample
from Vec2d import Vec2d

class TestSample(unittest.TestCase):

    # def test_equality(self):
    #         a = Vec2d(10, 10)
    #         b = Vec2d(10, 10)
            
    #         self.assertTrue(a == b)
    
    def test_dumps(self):
        sample = [
            Sample(
                Vec2d(0, 0),
                Vec2d(0, 0),
                Vec2d(0, 0),
                0
            ),
            Sample(
                Vec2d(1, 1),
                Vec2d(1, 1),
                Vec2d(1, 1),
                1
            ),
            Sample(
                Vec2d(2, 2),
                Vec2d(2, 2),
                Vec2d(2, 2),
                2
            ),
        ]
        print(Sample.serialize_array(sample))

suite = unittest.TestLoader().loadTestsFromTestCase(TestSample)
unittest.TextTestRunner(verbosity=2).run(suite)
