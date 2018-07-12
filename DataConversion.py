import GrooveDetection


class IrregularAudio:

    def __init__(self, groove=GrooveDetection.Groove):

        self.data = groove_to_irregular_audio(groove)

    def __len__(self):

        return len(self.data)

    def __add__(self, other):

        self.data.extend(other)

    def get_amplitudes(self):

        return [point[0] for point in self.data]

    def get_times(self):

        return [point[1] for point in self.data]


class Audio:

    def __init__(self, irregular_audio=IrregularAudio):

        normalized_audio = normalize_audio(irregular_audio.data)
        # To do: implement irregular sampling.
        self.data = normalized_audio

    def __len__(self):

        return len(self.data)

    def __add__(self, other):

        self.data.extend(other)

    def get_amplitudes(self):

        return [sample[0] for sample in self.data]

    def get_times(self):

        return [sample[1] for sample in self.data]


def groove_to_irregular_audio(groove=GrooveDetection.Groove):

    irregular_audio = list()
    amplitude = 0
    time = 0
    theta = 0
    dif_rhos = list()
    dif_theta = list()
    rhos = groove.get_rho_data()
    thetas = groove.get_theta_data()

    for i in range(len(rhos)-1):

        dif_rhos.append(rhos[i+1] - rhos[i])

    for i in range(len(thetas)-1):

        dif_theta.append(thetas[i+1] - thetas[i])

    for i in range(len(groove.angular_data)-1):

        amplitude = amplitude + dif_rhos[i]
        theta = theta + dif_theta[i]
        time = time + theta_to_time(theta, 1)
        irregular_audio.append((amplitude, time))

    return irregular_audio


def theta_to_time(theta, rotation):

    return rotation*theta/4680


# To do: deprecate?
def rho_to_amplitude(rho, time, slope, alpha=1):

    """ This function requires a bias, since we start at the max and end at the min.
    """

    return (rho + slope*time)/alpha


def normalize_audio(audio_data):

    amplitudes = [sample[0] for sample in audio_data]
    times = [sample[1] for sample in audio_data]
    max_amplitude = max(amplitudes)
    normalized_amplitudes = [sample/max_amplitude for sample in amplitudes]
    normalized_audio = list()

    for i in range(len(audio_data)):
        normalized_audio.append((normalized_amplitudes[i], times[i]))

    return normalized_audio




