import utils
import random
import matplotlib.pyplot as plt

class SampleVisualizer:
    def __init__(self, samples=[], rand_sample_len=None):
        self.samples = samples

        if rand_sample_len is not None:
            self.samples = self.gen_rand_samples(rand_sample_len)

    def plot_meas(self, meas):
        assert meas in utils.SAMPLE_ATTRIBUTES, "Measurement doesn't exist"
        assert type(getattr(self.samples[0], meas)) == utils.Vec2d, "Must use Vec2d type measurement"

        x = [getattr(v, meas).x for v in self.samples]
        y = [getattr(v, meas).y for v in self.samples]
        
        plt.plot(x, y, 'ro')
        plt.show()

    def gen_rand_samples(self, rand_sample_len):
        samp = []
        for i in range(rand_sample_len):
            x_rand = random.random()
            y_rand = random.random()

            s = utils.Vec2d(x_rand, y_rand)

            samp.append(utils.Sample(s, s, s, 10))

        return samp
        
if __name__ == '__main__':
    v = SampleVisualizer(rand_sample_len=400)

    v.plot_meas('pos')
    plt.show()



