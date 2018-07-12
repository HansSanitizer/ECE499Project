import GrooveDetection
import numpy as np


class IrregularAudio:

    def __init__(self, groove=GrooveDetection.Groove):

        self.data = groove_to_irregular_audio(groove)

    def __len__(self):

        return len(self.data)

    def __add__(self, other):

        self.data.extend(other)

    def get_amplitude_axis(self):

        return [sample[0] for sample in self.data]

    def get_time_axis(self):

        return [sample[1] for sample in self.data]


class Audio:

    def __init__(self, irregular_audio=IrregularAudio):

        # To do: implement irregular sampling.
        self.data = normalize_audio(irregular_audio.data)

    def __len__(self):

        return len(self.data)

    def __add__(self, other):

        self.data.extend(other)

    def get_amplitude_axis(self):

        return [sample[0] for sample in self.data]

    def get_time_axis(self):

        return [sample[1] for sample in self.data]


def groove_to_irregular_audio(groove=GrooveDetection.Groove):

    rho_diffs = calc_diffs(groove.get_rho_axis())
    theta_diffs = calc_diffs(groove.get_theta_axis())

    irregular_audio = list()
    amplitude = 0
    time = 0
    theta = 0

    for i in range(len(groove.angular_data)-1):

        amplitude = amplitude + rho_diffs[i]
        theta = theta + theta_diffs[i]
        time = time + theta_to_time(theta, 1)
        irregular_audio.append((amplitude, time))

    return irregular_audio


def calc_diffs(data):

    diffs = list()

    for i in range(len(data)-1):
        diffs.append(data[i+1] - data[i])

    return diffs

# To do: verify.
def theta_to_time(theta, rotation):

    return rotation*theta/4680


# To do: deprecate?
def rho_to_amplitude(rho, time, slope, alpha=1):

    """ This function requires a bias, since we start at the max and end at the min.
    """

    return (rho + slope*time)/alpha


def normalize_audio(audio_data):
    """
    Normalizes audio. (min = 0 and max = 1)

    :param audio_data:
    :return:
    """

    amplitudes = [sample[0] for sample in audio_data]
    times = [sample[1] for sample in audio_data]

    min_amplitude = min(amplitudes)
    shifted_amplitudes = [sample + np.abs(min_amplitude) for sample in amplitudes]

    max_amplitude = max(shifted_amplitudes)
    normalized_amplitudes = [sample/max_amplitude for sample in shifted_amplitudes]

    normalized_audio = list()

    for i in range(len(audio_data)):
        normalized_audio.append((normalized_amplitudes[i], times[i]))

    return normalized_audio




