"""
---
name: sound.py
description: Sound package file
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
change-log:
  2019-01-29:
  - version: 0.01
    Added: Starting a new package.
"""

from math import pi, sin
from pyaudio import PyAudio


class Sound():
    """
    description:
    """

    __version__ = '0.01'

    def __init__(self):
        self.bitrate = 44100  # Frames per second (frame rate / frameset)
        self.length = 0.015  # Sound duration (seconds)
        self.frames = int(self.bitrate * self.length)
        self.restframes = self.frames % self.bitrate
        self.open()

    def open(self):
        """
        description:
        """
        self.socket = PyAudio()
        self.stream = self.socket.open(
            format=self.socket.get_format_from_width(1),
            channels=1,
            rate=self.bitrate,
            output=True)

    def close(self):
        """
        description:
        """
        self.stream.stop_stream()
        self.stream.close()
        self.socket.terminate()

    def wave(self, frequency, length=0.015):
        """
        description:
        """
        self.length = length
        self.frames = int(self.bitrate * self.length)
        self.restframes = self.frames % self.bitrate
        wave = ''
        if frequency > self.bitrate:
            self.bitrate = frequency + 100
        for i in range(self.frames):
            wave += chr(int(sin(i / ((self.bitrate / frequency) / pi))
                            * 127 + 128))
        for _ in range(self.restframes):
            wave += chr(128)
        return wave

    def tone(self, frequency):
        """
        description:
        """
        sample = self.wave(frequency)
        self.stream.write(sample)

    def demo(self):
        """
        description:
        """
        for _ in range(2):
            sample = self.wave(587.33)
            self.stream.write(sample)
            sample = self.wave(783.99)
            self.stream.write(sample)
            sample = self.wave(392)
            self.stream.write(sample)
            sample = self.wave(880)
            self.stream.write(sample)
