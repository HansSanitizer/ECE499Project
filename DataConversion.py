import GrooveDetection
import wave
import struct
import scipy.signal as signal
import numpy as np


# To do: this class is likely to transform into the Audio class.
class IrregularAudio:

    def __init__(self, groove=None, rotation=1):

        if groove is None:

            self.data = list()

        elif isinstance(groove, GrooveDetection.Groove):

            self.data = groove_to_velocity(rotation, time_axis_unique(groove.angular_data))

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

    # this implementation is hacky
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

    def __init__(self, sample_rate=48000, irregular_audio=None):

        if irregular_audio is None:
            self.data = list()
        elif isinstance(irregular_audio, IrregularAudio):
            audio_interp = voroni_interp(sample_rate, irregular_audio)
            audio_filtered = filter_voroni(audio_interp)
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


def time_axis_unique(data):
    """
    We have issues with duplicates in the time axis causing div 0 errors down the line.

    :param data: groove.angular_data
    :return: data points with a unique time axis-value
    """

    seen = set()
    unique = list()

    for x in data:
        if x[1] not in seen:
            unique.append(x)
            seen.add(x[1])

    return unique


# assuming that capture is actually working, our problems probably start here.
def groove_to_velocity(rotation, data):

    return angular_to_velocity([point[0] for point in data], [theta_to_time(point[1], rotation) for point in data])


# To do: verify.
def theta_to_time(theta, rotation):

    return rotation*theta/(1.3*2*np.pi)


def angular_to_velocity(rhos, times):

    if len(rhos) != len(times):
        raise RuntimeError(' inputs must be equal in length.')

    velocity = list()

    window_width = 15
    n_points = len(rhos)
    n_chunks = n_points/window_width

    for i in range(1, n_chunks):
        points, center, duration = get_chunk(i, rhos, times, window_width)
        # To do: figure out why you get a poorly conditioned warning.
        poly = np.polyfit([point[0] for point in points], [point[1] for point in points], 4)
        poly_der = np.polyder(poly)
        # Sample velocity at multiples of sampling period, not the center of the window.
        velocity.append(np.polyval(poly_der, times[center]))

    return velocity


def get_chunk(i, rhos, times, width=15):

    center = width/2
    wing_size = center - 1
    chunk_center = i * center
    start = chunk_center - wing_size
    end = chunk_center + wing_size
    duration = times[end] - times[start]
    points = [(rhos[i], times[i]) for i in range(start, chunk_center - 1)]
    points.append((rhos[chunk_center], times[chunk_center]))
    points.extend([(rhos[i], times[i]) for i in range(chunk_center + 1, end)])

    return points, chunk_center, duration


def normalize_amplitudes(amplitudes):
    max_amplitude = max(np.abs(amplitudes))
    return [n/max_amplitude for n in amplitudes]


def audio_to_wave(audio, name='recovered_audio'):

    audio_packed = pack_audio(audio)
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


# <under scrutiny>
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
def sample_voroni(sample_rate=48000, audio_data=None):

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


def filter_voroni(data):

    sampled_audio = sample_voroni(48000, data)
    filtered_audio = filter_lp(sampled_audio)

    return filtered_audio
# </under scrutiny>


def filter_lp(data, order=3, wn=0.5):

    b, a = signal.butter(order, wn)
    filtered_audio = signal.lfilter(b, a, data)

    return list(filtered_audio)
