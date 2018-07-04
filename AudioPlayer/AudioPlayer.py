import pyaudio
import wave


class AudioPlayer:

    def __init__(self):

        self.CHUNK = 1024
        self.path = str()
        self.p = pyaudio.PyAudio()

    def __del__(self):

        self.p.terminate()

    def load(self, path):

        self.path = path
        self.wf = wave.open(path, 'rb')

    def play(self):

        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)

        self.data = self.wf.readframes(self.CHUNK)

        while len(self.data) > 0:

            self.stream.write(self.data)

            self.data = self.wf.readframes(self.CHUNK)

        self.stream.stop_stream()

        self.stream.close()
