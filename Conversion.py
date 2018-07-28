import Detection
import wave
import struct
import scipy.signal as signal
import numpy as np
import Data


class Stylus:

    def __init__(self, rtime_data=None, rotation=1):

            self.data = rtime_to_velocity(rtime_data)

    def __len__(self):

        return len(self.data)

    def append(self, other):

        if isinstance(other, Stylus):
            self.data.extend(other.data)
        else:
            raise TypeError(' must append Stylus object.')

    def get_velocity_axis(self):

        return [sample[0] for sample in self.data]

    def get_time_axis(self):

        return [sample[1] for sample in self.data]


class Audio:

    def __init__(self, sample_rate=48000, irregular_audio=None):

        if irregular_audio is None:
            self.data = list()
        elif isinstance(irregular_audio, Stylus):
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


# To do: this may be unnecessary because of the poly fit method.
def time_axis_unique(angular_data):
    """
    We have issues with duplicates in the time axis causing div 0 errors down the line.

    :param angular_data: groove.angular_data
    :return: data points with a unique time axis-value
    """

    seen = set()
    unique = list()

    for x in angular_data:
        if x[1] not in seen:
            unique.append(x)
            seen.add(x[1])

    return unique


def rtime_to_velocity(rtime_data, sample_rate=48000, threshold=1):
    """
    Converts time data to resampled velocity data.
    :param rtime_data:
    :param sample_rate:
    :return:
    """
    velocities = list()

    window_width = 15
    n_points = len(rtime_data)
    n_chunks = n_points/window_width

    # t = 0

    t = Data.t_in_points(rtime_data)
    r = Data.r_in_points(rtime_data)

    for i in range(0, len(rtime_data)-1):

        v = (r[i + 1] - r[i])/(t[i + 1] - t[i])
        t_average = (t[i] + t[i+1])/2
        velocities.append((v, t_average))

    # for i in range(1, n_chunks):
    #     chunk, center, duration = get_chunk(i, rtime_data, window_width)
    #     t = t + duration/2
    #     # To do: figure out why you get a poorly conditioned warning.
    #     poly = np.polyfit(Data.t_in_points(chunk), Data.r_in_points(chunk), 3)
    #     poly_der = np.polyder(poly)
    #     # To do: sample velocity at multiples of sampling period, not the center of the window.
    #     # resample_poly(poly_der, duration)
    #     velocities.append((np.polyval(poly_der, t), t))

    return velocities


def get_chunk(i, rtime_data, width=15):

    center = width/2
    wing_size = center - 1
    chunk_center = i * center
    start = chunk_center - wing_size
    end = chunk_center + wing_size
    chunk = rtime_data[start:end]
    t_final = Data.t_in_points(chunk)[len(chunk) - 1]
    t_initial = Data.t_in_points(chunk)[0]
    duration = t_final - t_initial

    return chunk, chunk_center, duration


def resample_poly(p, duration, time_bias):

    # To do: implement

    return


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


def filter_lp(data, order=3, wn=0.5):

    b, a = signal.butter(order, wn)
    filtered_audio = signal.lfilter(b, a, data)

    return list(filtered_audio)
