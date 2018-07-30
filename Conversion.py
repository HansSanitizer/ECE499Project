import Detection
import wave
import struct
import scipy.signal as signal
import numpy as np
import Data


class Stylus:

    def __init__(self, rtime_data=list()):
        """

        Object that represents the phonograph stylus that is essentially a container for time-velocity data.

        :param rtime_data: list of points in r-time coordinates.
        """

        self.data = rtime_to_velocity(rtime_data)

    def __len__(self):

        return len(self.data)

    def append(self, other):

        if isinstance(other, Stylus):
            self.data.extend(other.data)
        else:
            raise TypeError(' must append Stylus object.')

    def get_velocity_axis(self):

        return [data[0] for data in self.data]

    def get_time_axis(self):

        return [data[1] for data in self.data]


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


def rtime_to_velocity(rtime_data):
    """

    Converts rtime data to velocity data.

    :param rtime_data: list of points in r-time
    :return: list of velocity data as tuple in form of (time, velocity)
    """

    # Commented lines are elements of a more sophisticated implementation that was abandoned due to time constraints.
    velocities = list()

    # window_width = 15
    # n_points = len(rtime_data)
    # n_chunks = n_points/window_width

    # t = 0

    t = Data.get_t_axis(rtime_data)
    r = Data.get_r_axis(rtime_data)

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


# def get_chunk(i, rtime_data, width=15):
#     """
#
#     Returns a chunk of rtime data from a larger data set. For abandoned implementation of rtime_to_velocity.
#
#     :param i:
#     :param rtime_data:
#     :param width:
#     :return:
#     """
#
#     center = width/2
#     wing_size = center - 1
#     chunk_center = i * center
#     start = chunk_center - wing_size
#     end = chunk_center + wing_size
#     chunk = rtime_data[start:end]
#     t_final = Data.get_t_axis(chunk)[len(chunk) - 1]
#     t_initial = Data.get_t_axis(chunk)[0]
#     duration = t_final - t_initial
#
#     return chunk, chunk_center, duration


def audio_to_wave(audio, file_name='recovered_audio'):
    """

    Converts an audio object to a wave-file.

    :param audio: audio object
    :param file_name: string
    :return: nothing
    """

    audio_packed = pack_audio(audio)
    audio_packed_str = packed_to_string(audio_packed)
    f = wave.open(file_name + '.wav', 'w')
    f.setnchannels(1)
    f.setsampwidth(4)
    f.setframerate(48000)
    f.writeframes(audio_packed_str)
    f.close()

    return


def pack_audio(amplitudes):
    """

    Returns byte string of packed audio.

    :param amplitudes:
    :return:
    """

    return [struct.pack('>f', amplitude) for amplitude in amplitudes]


def packed_to_string(packed_audio):


    audio_packed_str = str()

    for element in packed_audio:
        audio_packed_str = audio_packed_str + str(element)

    return audio_packed_str


def filter_lp(data, order=3, wn=0.5):
    """

    Applies a low-pass filter on audio data.

    :param data: audio data
    :param order:
    :param wn:
    :return: filtered audio-data
    """

    b, a = signal.butter(order, wn)
    filtered_audio = signal.lfilter(b, a, data)

    return list(filtered_audio)
