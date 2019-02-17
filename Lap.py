import csv
import sys
import os


class Checkpoint:
    def __init__(self, number, node1, node2, samples=[]):
        self.number = number   # Integer
        self.node1 = node1     # Vec2d
        self.node2 = node2     # Vec2d
        self.samples = samples[:] # Array of Sample
        self.time = 0

    def __repr__(self):
        return '''
Number: {number}
Node1: {node1}
Node2: {node2}
Samples: {samples}
Time: {time}
'''.format(
    number=self.number,
    node1=self.node1,
    node2=self.node2,
    samples=self.samples,
    time=self.time
    )

    def entry_velocity(self):
        assert self.samples, 'Samples array is empty'
        return self.samples[0].vel

    def exit_velocity(self):
        assert self.samples, 'Samples array is empty'
        return self.samples[-1].vel

    def parse_from_server(self, json):
        pass

    def contains(self, sample):
        return sample in self.samples

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

        if o1 == 0 and self.__on_segment(p1, p2, q1):
            return True
        if o2 == 0 and self.__on_segment(p1, q2, q1):
            return True
        if o3 == 0 and self.__on_segment(p2, p1, q2):
            return True
        if o4 == 0 and self.__on_segment(p2, q1, q2):
            return True
        
        return False


    def __on_segment(self, p, q, r):
        if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
            return True
        return False

    def __orientation(self, p, q, r):
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
        self.populate_checkpoint_samples()

    def __repr__(self):
        return '''
Path: {path}

Checkpoints: {checkpoints}
        '''.format(path=self.path, checkpoints=self.checkpoints)

    # Checkpoints is the list of checkpoint lines
    # This will get the first node after the checkpoint line is crossed
    # and grab any addtl samples until the next checkpoint is hit
    def populate_checkpoint_samples(self):
        i = -1
        search = 0

        for (sample, nextsample) in zip(self.path, self.path[1::]):
            search_checkpoint = self.checkpoints[search % len(self.checkpoints)]
            if (search_checkpoint.crossedCheckpoint(sample, nextsample)
                and not search_checkpoint.contains(sample)):
                # Line was crossed
                i = i + 1
                search = search + 1
                if (i >= len(self.checkpoints)):
                    # Splice the samples that weren't used yet
                    self.path = self.path[self.path.index(nextsample):]
                    break
            if i >= 0:
                self.checkpoints[i].samples.append(nextsample)
        
        self.compile_lap_times()

    def compile_lap_times(self):
        for checkpoint in self.checkpoints:
            # Calculate the time of the "Checkpoint Samples"
            checkpoint.time = checkpoint.samples[-1] - checkpoint.samples[0]
