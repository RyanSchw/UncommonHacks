import Vec2d
import Sample
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class SampleVisualizer:
    def __init__(self, samples=[], rand_sample_len=None):
        self.samples = samples

        if rand_sample_len is not None:
            self.samples = self.gen_rand_samples(rand_sample_len)

    def plot_track(self, max_vel=1):
        x = [v.pos.x for v in self.samples]
        y = [v.pos.y for v in self.samples]
        col = cm.rainbow([v.vel.mag() / max_vel for v in self.samples])
        
        plt.scatter(x, y, c=col, s=50)
        plt.show()

    def gen_rand_samples(self, rand_sample_len):
        samp = []
        for i in range(rand_sample_len):

            p = utils.Vec2d.rand()
            v = utils.Vec2d.rand()
            a = utils.Vec2d.rand()

            samp.append(utils.Sample(p, v, a, 10))

        return samp
        
if __name__ == '__main__':
    v = SampleVisualizer(rand_sample_len=400)

    v.plot_track()
    plt.show()



