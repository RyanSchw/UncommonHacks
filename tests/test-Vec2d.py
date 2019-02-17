import unittest
from utils import Vec2d

class TestVec2d(unittest.TestCase):

    def test_equality(self):
            a = Vec2d(10, 10)
            b = Vec2d(10, 10)
            
            self.assertTrue(a == b)
    
    def test_not_equality(self):
        a = Vec2d(0, 0)
        b = Vec2d(10, 10)
        
        self.assertTrue(a != b)

    def test_addition(self):
        a = Vec2d(10, 10)
        b = Vec2d(10, 10)
        
        c = Vec2d(20, 20)

        self.assertTrue(a + b == c)

    def test_subtraction(self):
        a = Vec2d(10, 10)
        b = Vec2d(10, 10)
        
        c = Vec2d(0, 0)

        self.assertTrue(a - b == c)

    def test_multiplication(self):
        a = Vec2d(10, 10)
        b = 10
        
        c = Vec2d(100, 100)

        self.assertTrue(a * b == c)

    def test_division(self):
        a = Vec2d(10, 10)
        b = 5.2
        
        c = Vec2d(10/ 5.2, 10 / 5.2)

        self.assertTrue(a / b == c)

    def test_mag(self):
        a = Vec2d(3, 4)
        b = 5

        self.assertTrue(a.mag() == b)

    def test_unit_vector(self):
        a = Vec2d(3, 4).unit()
        b = Vec2d(3/5, 4/5)

        self.assertTrue(a == b)

suite = unittest.TestLoader().loadTestsFromTestCase(TestVec2d)
unittest.TextTestRunner(verbosity=2).run(suite)
