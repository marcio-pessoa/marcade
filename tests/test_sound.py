"""
---
name: test_sound.py
description: Test Sound Class
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys


class TestSound(unittest.TestCase):
    """ Test Sound Class """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pyaudio = MagicMock()
        cls.modules_patcher = patch.dict(sys.modules, {
            'pyaudio': cls.mock_pyaudio,
        })
        cls.modules_patcher.start()

        # pylint: disable=import-outside-toplevel
        from src.sound import Sound
        cls.Sound = Sound

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.sound = self.Sound()

    def test_initialization(self):
        """ Test initialization """
        self.sound.socket.open.assert_called_once()
        self.assertEqual(self.sound.bitrate, 44100)

    def test_tone(self):
        """ Test tone """
        self.sound.tone(440)
        self.sound.stream.write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
