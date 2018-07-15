import GrooveDetection


class IrregularAudio:

    def __init__(self, groove=None, rotation=1):

        if groove is None:
            self.data = list()
        elif isinstance(groove, GrooveDetection.Groove):
            self.data = groove_to_irregular_audio(rotation, groove)
        else:
            raise TypeError

    def __len__(self):

        return len(self.data)

    def extend(self, other):

        if isinstance(other, IrregularAudio):
            self.data.extend(other.data)
        else:
            raise TypeError

    def get_amplitude_axis(self):

        return [sample[0] for sample in self.data]

    def get_time_axis(self):

        return [sample[1] for sample in self.data]


# To do: finish this class
class Audio:

    def __init__(self, irregular_audio=None):

        if irregular_audio is None:
            self.data = list()
        elif irregular_audio is IrregularAudio:
            # To do: implement irregular sampling.
            self.data = IrregularAudio
        else:
            raise TypeError

    def __len__(self):

        return len(self.data)

    def __add__(self, other):

        if other is Audio:
            self.data.extend(other.data)
        else:
            raise TypeError

    def get_amplitude_axis(self):

        return [sample[0] for sample in self.data]

    def get_time_axis(self):

        return [sample[1] for sample in self.data]


def groove_to_irregular_audio(rotation, groove=GrooveDetection.Groove):

    times = [theta_to_time(theta, rotation) for theta in groove.get_theta_axis()]
    amplitudes = [rho_to_amplitude(rho, times[i], groove.slope) for i, rho in enumerate(groove.get_rho_axis())]
    irregular_audio = [(amplitudes[i], times[i]) for i in range(len(groove.angular_data))]

    # This method makes no sense.
    # # are these ordered correctly?
    # rho_diffs = calc_diffs(groove.get_rho_axis())
    # theta_diffs = calc_diffs(groove.get_theta_axis())
    #
    # irregular_audio = list()
    # amplitude = 0
    # time = 0
    # theta = 0
    #
    # for i in range(len(groove.angular_data)-1):
    #
    #     amplitude = amplitude + rho_diffs[i]
    #     theta = theta + theta_diffs[i]
    #     time = time + theta_to_time(theta, 1)
    #     irregular_audio.append((amplitude, time))

    return irregular_audio


# To do: verify, specifically is the rotation parameter necessary?
def theta_to_time(theta, rotation):

    return rotation*theta/4680


def rho_to_amplitude(rho, time, slope, alpha=1):

    return (rho + slope*time)/alpha
