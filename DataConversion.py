import GrooveDetection

class IrregularAudio:

    def __init__(self, groove):

        self.data = groove_to_irregular_audio(groove)

    def __len__(self):

        return len(self.data)


class Audio:

    def __init__(self, irregular_audio):

        # To do: implement irregular sampling.
        self.data = irregular_audio

    def __len__(self):

        return len(self.data)


def groove_to_irregular_audio(groove, alpha=1):

    irregular_audio = list()

    for point in groove.angular_data:

        time = point[1]/13
        amplitude = (point[0] + groove.slope*time)/alpha
        irregular_audio.append((amplitude, time))

    return irregular_audio
