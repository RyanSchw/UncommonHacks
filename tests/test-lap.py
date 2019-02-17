import unittest
import mock
from Lap import Checkpoint, Run
from Vec2d import Vec2d
from Sample import Sample

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

class TestRun(unittest.TestCase):
    def test_funtionality(self):
        path = [
            Sample(
                Vec2d(0, 0),
                Vec2d(0, 0), Vec2d(0, 0), 0
            ),
            Sample(
                Vec2d(1, 1),
                Vec2d(0, 0), Vec2d(0, 0), 1
            ),
            Sample(
                Vec2d(2, 0),
                Vec2d(0, 0), Vec2d(0, 0), 2
            ),
            Sample(
                Vec2d(3, 3),
                Vec2d(0, 0), Vec2d(0, 0), 3
            ),
            Sample(
                Vec2d(4, 4),
                Vec2d(0, 0), Vec2d(0, 0), 4
            ),
            Sample(
                Vec2d(-1, 0),
                Vec2d(0, 0), Vec2d(0, 0), 5
            )
        ]
        checkpoints = [
            Checkpoint(
                1,
                Vec2d(1, 0),
                Vec2d(1, 2)
            ),
            Checkpoint(
                2,
                Vec2d(2.5, 0),
                Vec2d(2.5, 3)
            )
        ]
        lap = Run(path, checkpoints)

        self.assertEqual(lap.checkpoints[0].samples[0].pos, Vec2d(1, 1))

    @mock.patch('Lap.Run.populate_checkpoint_samples')
    def test_lap_times(self, mocked):
        mocked.return_value = 1
        lap = Run(None, [Checkpoint(None, None, None, [
            Sample(
                None, None, None,
                2
            ),
            Sample(
                None, None, None,
                5
            )
        ])])

        lap.compile_lap_times()
        res = lap.checkpoints[0].time

        self.assertEqual(res, 3)


# Display all the tests passing
suite = unittest.TestLoader().loadTestsFromTestCase(TestCheckpoint)
unittest.TextTestRunner(verbosity=2).run(suite)
suite = unittest.TestLoader().loadTestsFromTestCase(TestRun)
unittest.TextTestRunner(verbosity=2).run(suite)