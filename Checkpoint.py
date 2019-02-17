import csv
import sys
import os


class Checkpoint:
    def __init__(self, number, node1, node2, samples=[]):
        self.number = number
        self.node1 = node1  # Vec2d
        self.node2 = node2  # Vec2d
        self.samples = samples # Array of Sample

    # Checkpoints is the list of checkpoint lines
    def sort_samples(path, checkpoints):
        start = 0
        samples = []
        for (sample, nextsample) in zip(path, path[1::]):
            # Check if point has crossed a checkpoint
            for checkpoint in checkpoints:
                if (Checkpoint.__crossedCheckpoint(checkpoint, sample, nextsample)):
                    print('Line was crossed!!')
                    # Create new checkpoint item
                else:
                    print('Line was not crossed')
                    # Append onto the Checkpoint created when line was crossed
            print(sample)
            print(nextsample)

    def crossedCheckpoint(checkpoint, sample, nextsample):
        # See if lines intersect
        # https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        p1 = checkpoint.node1
        q1 = checkpoint.node2
        p2 = sample.pos
        q2 = nextsample.pos

        o1 = Checkpoint.__orientation(p1, q1, p2)
        o2 = Checkpoint.__orientation(p1, q1, q2)
        o3 = Checkpoint.__orientation(p2, q2, p1)
        o4 = Checkpoint.__orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and Checkpoint.__on_segment(p1, p2, q1):
            return True
        if o2 == 0 and Checkpoint.__on_segment(p1, q2, q1):
            return True
        if o3 == 0 and Checkpoint.__on_segment(p2, p1, q2):
            return True
        if o4 == 0 and Checkpoint.__on_segment(p2, q1, q2):
            return True
        
        return False


    def __on_segment(p, q, r):
        if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
            return True
        return False

    def __orientation(p, q, r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

        if val == 0:
            return 0
        
        if val > 0:
            return 1
        return 2
