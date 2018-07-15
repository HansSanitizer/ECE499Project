import GrooveDetection
import wave
import struct
import scipy.signal as signal


class IrregularAudio:

    def __init__(self, groove=None, rotation=1):

        if groove is None:

            self.data = list()

        elif isinstance(groove, GrooveDetection.Groove):

            self.data = groove_to_irregular_audio(rotation, groove)

        else:
            raise TypeError(' must initialize from Groove object.')

    def __len__(self):

        return len(self.data)

    def append(self, other):

        if isinstance(other, IrregularAudio):
            self.data.extend(other.data)
        else:
            raise TypeError(' must append IrregularAudio object.')

    def get_amplitude_axis(self):

        return [sample[0] for sample in self.data]

    def get_time_axis(self):

        return [sample[1] for sample in self.data]

    def get_max_gap(self):

        gaps = list()

        for i in range(1, len(self.data) - 1):
            this_data = self.data[i - 1]
            next_data = self.data[i]

            this_time = this_data[1]
            next_time = next_data[1]

            gaps.append(next_time - this_time)

        return max(gaps)


# To do: finish this class
class Audio:

    def __init__(self, sample_rate, irregular_audio=None):

        if irregular_audio is None:
            self.data = list()
        elif isinstance(irregular_audio, IrregularAudio):
            audio_interp = voroni_interp(48000, irregular_audio)
            audio_filtered = filter_audio(audio_interp)
            self.data = audio_filtered
        else:
            raise TypeError(' must initialize from IrregularAudio object.')

    def __len__(self):

        return len(self.data)

    def append(self, other):

        if isinstance(other, Audio):
            # Ignore the warning that may show on the next line, this is intentional.
            self.data.append(other.data)
        else:
            raise TypeError(' must append Audio object.')


def groove_to_irregular_audio(rotation, groove=GrooveDetection.Groove):

    times = [theta_to_time(theta, rotation) for theta in groove.get_theta_axis()]
    amplitudes = [rho_to_amplitude(rho, times[i], groove.slope) for i, rho in enumerate(groove.get_rho_axis())]
    irregular_audio = [(amplitudes[i], times[i]) for i in range(len(groove.angular_data))]

    return irregular_audio


# To do: verify, specifically is the rotation parameter necessary?
def theta_to_time(theta, rotation):

    # return rotation*theta/4680
    return rotation*theta/8.293804605


def rho_to_amplitude(rho, time, slope, alpha=1):

    return (rho + slope*time)/alpha


# Temporarily takes an IrregularAudio object as input.
# This will be changed in future to take an Audio object.
# Also, this function will barely work if at all until it's fully implemented.
def audio_to_wave(audio, name='recovered_audio'):

    amplitudes = audio.get_amplitude_axis()
    audio_packed = pack_audio(amplitudes)
    audio_packed_str = packed_to_string(audio_packed)
    f = wave.open(name + '.wav', 'w')
    f.setnchannels(1)
    f.setsampwidth(4)
    f.setframerate(48000)
    f.writeframes(audio_packed_str)
    f.close()

    return


def pack_audio(amplitudes):

    return [struct.pack('>f', amplitude) for amplitude in amplitudes]


def packed_to_string(packed_audio):

    audio_packed_str = str()

    for element in packed_audio:
        audio_packed_str = audio_packed_str + str(element)

    return audio_packed_str


# This is producing a set of step-functions.
def voroni_interp(sample_rate, audio=IrregularAudio()):

    data = audio.data
    sampling_period = 1/float(sample_rate)
    interp_audio = list()

    for i in range(1, len(data)):

        this_point = data[i-1]
        next_point = data[i]

        this_time = this_point[1]
        this_amplitude = this_point[0]

        next_time = next_point[1]
        next_amplitude = next_point[0]

        mid_point_time = this_time + (next_time - this_time)/2

        if (mid_point_time/sampling_period) % 2 != 0:
            mid_point_amplitude = (this_amplitude + next_amplitude)/2
        else:
            mid_point_amplitude = next_amplitude

        points = this_point, (mid_point_amplitude, mid_point_time), next_point

        interp_audio.extend(points)

    return interp_audio


# This will sample the step functions created by voroni_interp.
# Think I just invalidated this. theta_to_time was incorrect.
def sample_audio(sample_rate=48000, audio_data=None):

    if audio_data is None:
        raise TypeError(' requires audio data.')

    initial_audio_data = audio_data[0]
    final_audio_data = audio_data[len(audio_data) - 1]

    initial_time = initial_audio_data[1]
    final_time = final_audio_data[1]

    audio_duration = final_time - initial_time

    times = [element[1] - initial_time for element in audio_data]
    amplitudes = [element[0] for element in audio_data]

    sample_period = 1/float(48000)
    n_samples = int(audio_duration / sample_period)
    samples = list()
    i = 0

    for n in range(n_samples):

        sample_instant = float(n*sample_period)

        while i < len(audio_data):

            if times[i] <= sample_instant < times[i + 1]:
                samples.append(amplitudes[i])
                i = i + 1
                break

            i = i + 1

    return samples


def filter_audio(data, order=3, wn=0.5):

    sampled_audio = sample_audio(48000, data)
    b, a = signal.butter(order, wn)
    filtered_audio = signal.lfilter(b, a, sampled_audio)

    return list(filtered_audio)
