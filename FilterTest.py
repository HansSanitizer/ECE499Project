import DataConversion
import numpy as np


def get_sin_sample(n, sample_period=1/float(48000), frequency=1000):

    return np.sin(n*sample_period*2*np.pi*frequency)


def get_samples(duration=5, sample_period=1/float(48000)):

    n_samples = int(duration/sample_period)
    samples = list()

    for n in range(0, n_samples-1):
        samples.append(get_sin_sample(n))

    return samples


samples = get_samples()
filtered_samples = DataConversion.filter_lp(samples)
DataConversion.audio_to_wave(samples, 'FilterTest_unfiltered')
DataConversion.audio_to_wave(filtered_samples, 'FilterTest_filtered')
