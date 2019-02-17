import unittest
from Checkpoint import Checkpoint
import Vec2d
import Sample

class TestCheckpoint(unittest.TestCase):
    def test_intersection(self):
        node1 = Vec2d(0, 0)
        node2 = Vec2d(2, 0)
        checkpoint = Checkpoint(1, node1, node2)

        sample1 = Sample(Vec2d(1, -1), Vec2d(0, 0), Vec2d(0, 0), 0)
        sample2 = Sample(Vec2d(1, 1), Vec2d(0, 0), Vec2d(0, 0), 1)

        self.assertTrue(checkpoint.crossedCheckpoint(sample1, sample2))
    
    def test_overlap(self):
        node1 = Vec2d(0, 0)
        node2 = Vec2d(2, 0)
        checkpoint = Checkpoint(1, node1, node2)

        sample1 = Sample(Vec2d(1, 0), Vec2d(0, 0), Vec2d(0, 0), 0)
        sample2 = Sample(Vec2d(3, 0), Vec2d(0, 0), Vec2d(0, 0), 1)

        self.assertTrue(checkpoint.crossedCheckpoint(sample1, sample2))

    def test_colinear(self):
        node1 = Vec2d(0, 0)
        node2 = Vec2d(2, 2)
        checkpoint = Checkpoint(1, node1, node2)

        sample1 = Sample(Vec2d(1, 0), Vec2d(0, 0), Vec2d(0, 0), 0)
        sample2 = Sample(Vec2d(3, 2), Vec2d(0, 0), Vec2d(0, 0), 1)

        self.assertFalse(checkpoint.crossedCheckpoint(sample1, sample2))

    def test_sequential(self):
        node1 = Vec2d(0, 0)
        node2 = Vec2d(2, 2)
        checkpoint = Checkpoint(1, node1, node2)

        sample1 = Sample(Vec2d(3, 3), Vec2d(0, 0), Vec2d(0, 0), 0)
        sample2 = Sample(Vec2d(4, 4), Vec2d(0, 0), Vec2d(0, 0), 1)

        self.assertFalse(checkpoint.crossedCheckpoint(sample1, sample2))

    def test_no_overlap(self):
        node1 = Vec2d(0, 0)
        node2 = Vec2d(1, 1)
        checkpoint = Checkpoint(1, node1, node2)

        sample1 = Sample(Vec2d(0, 3), Vec2d(0, 0), Vec2d(0, 0), 0)
        sample2 = Sample(Vec2d(3, 0), Vec2d(0, 0), Vec2d(0, 0), 1)

        self.assertFalse(checkpoint.crossedCheckpoint(sample1, sample2))

    def test_short_by_limit(self):
        node1 = Vec2d(0, 0)
        node2 = Vec2d(2, 2)
        checkpoint = Checkpoint(1, node1, node2)

        sample1 = Sample(Vec2d(3, 3), Vec2d(0, 0), Vec2d(0, 0), 0)
        sample2 = Sample(Vec2d(4, 6), Vec2d(0, 0), Vec2d(0, 0), 1)

        self.assertFalse(checkpoint.crossedCheckpoint(sample1, sample2))

    def test_point_on_line(self):
        node1 = Vec2d(0, 0)
        node2 = Vec2d(2, 2)
        checkpoint = Checkpoint(1, node1, node2)

        sample1 = Sample(Vec2d(1, 1), Vec2d(0, 0), Vec2d(0, 0), 0)
        sample2 = Sample(Vec2d(2, 3), Vec2d(0, 0), Vec2d(0, 0), 1)

        self.assertTrue(checkpoint.crossedCheckpoint(sample1, sample2))

# Display all the tests passing
suite = unittest.TestLoader().loadTestsFromTestCase(TestCheckpoint)
unittest.TextTestRunner(verbosity=2).run(suite)