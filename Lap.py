import csv
import sys
import os


class Checkpoint:
    def __init__(self, number, node1, node2, samples=[]):
        self.number = number   # Integer
        self.node1 = node1     # Vec2d
        self.node2 = node2     # Vec2d
        self.samples = samples # Array of Sample
        self.time = 0

    def parse_from_server(self, json):
        pass

    def crossedCheckpoint(self, sample, nextsample):
        # See if lines intersect
        # https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

        p1 = self.node1
        q1 = self.node2
        p2 = sample.pos
        q2 = nextsample.pos

        o1 = self.__orientation(p1, q1, p2)
        o2 = self.__orientation(p1, q1, q2)
        o3 = self.__orientation(p2, q2, p1)
        o4 = self.__orientation(p2, q2, q1)

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


class Run:
    def __init__(self, path, checkpoints):
        self.path = path
        self.checkpoints = checkpoints
        self.populate()

    # Checkpoints is the list of checkpoint lines
    def populate_checkpoint_samples(self):
        start = 0
        samples = []
        for (sample, nextsample) in zip(self.path, self.path[1::]):
            currentCheckpoint = 0
            # Check if point has crossed a checkpoint
            # Checkpoints are in order, so only need to look for the first one
            for checkpoint in self.checkpoints:
                if (checkpoint.crossedCheckpoint(sample, nextsample)):
                    print('Line was crossed!!')
                    currentCheckpoint = checkpoint
                currentCheckpoint.samples.push(sample)
        return samples
