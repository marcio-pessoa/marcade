"""
---
name: test_joystick.py
description: Test Joystick Class
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys

# Patcher needs to be at the module level to be accessible by both classes
mock_pygame = MagicMock()
modules_patcher = patch.dict(sys.modules, {'pygame': mock_pygame})

# We need to import the modules under test AFTER the patch is applied
modules_patcher.start()
# pylint: disable=import-outside-toplevel
from src.joystick import Joystick, detect
modules_patcher.stop()


class TestJoystick(unittest.TestCase):
    """ Test Joystick Class """

    def setUp(self):
        """ Set up test """
        modules_patcher.start()
        self.joystick = Joystick()

    def tearDown(self):
        """ Tear down test """
        modules_patcher.stop()

    def test_initialization(self):
        """ Test initialization """
        self.assertIsNone(self.joystick.identification())

    def test_identification(self):
        """ Test identification """
        mock_joystick_instance = MagicMock()
        mock_pygame.joystick.Joystick.return_value = mock_joystick_instance
        self.joystick.identification(0)
        self.assertEqual(self.joystick.identification(), 0)
        mock_joystick_instance.init.assert_called_once()


class TestDetect(unittest.TestCase):
    """ Test detect function """

    def setUp(self):
        """ Set up test """
        modules_patcher.start()

    def tearDown(self):
        """ Tear down test """
        modules_patcher.stop()

    def test_detect(self):
        """ Test detect """
        mock_pygame.joystick.get_count.return_value = 1
        self.assertEqual(detect(), (0,))
        mock_pygame.joystick.get_count.return_value = 0
        self.assertFalse(detect())


if __name__ == '__main__':
    unittest.main()
