"""
---
name: test_arcade.py
description: Test Arcade Class
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys


class TestArcade(unittest.TestCase):
    """ Test Arcade Class """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()
        cls.mock_joystick = MagicMock()
        cls.mock_game_template = MagicMock()

        # Configure mock constants to have specific values
        cls.mock_pygame.locals.KEYDOWN = 1
        cls.mock_pygame.locals.K_ESCAPE = 2
        cls.mock_pygame.locals.QUIT = 3
        cls.mock_pygame.locals.KEYUP = 4
        cls.mock_pygame.locals.DOUBLEBUF = 5

        cls.modules_patcher = patch.dict(sys.modules, {
            'pygame': cls.mock_pygame,
            'pygame.locals': cls.mock_pygame.locals,
            'src.joystick': cls.mock_joystick,
            'src.game_template': cls.mock_game_template,
        })
        cls.modules_patcher.start()

        # pylint: disable=import-outside-toplevel
        from src.arcade import Arcade
        cls.Arcade = Arcade

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.game_class = MagicMock()
        self.game_class.__name__ = "TestGame"
        self.game_class.__version__ = "1.0"
        self.arcade = self.Arcade(self.game_class)

    def test_initialization(self):
        """ Test initialization """
        self.assertFalse(self.arcade.running)
        self.game_class.assert_not_called()

    def test_run_loop(self):
        """ Test run loop """
        # Mock __check_event to run the loop only once
        def stop_loop_side_effect():
            self.arcade._Arcade__running = False
            return (set(), None)

        self.arcade._Arcade__check_event = MagicMock(
            side_effect=stop_loop_side_effect)

        self.arcade.run()

        # Check that game methods were called
        self.game_class.return_value.control.assert_called_once()
        self.game_class.return_value.update.assert_called_once()

    def test_escape_key_stops_running(self):
        """ Test escape key stops running """
        self.arcade._Arcade__running = True
        event = MagicMock()
        event.type = self.mock_pygame.locals.KEYDOWN
        event.key = self.mock_pygame.locals.K_ESCAPE
        self.mock_pygame.event.get.return_value = [event]
        self.arcade._Arcade__check_event()
        self.assertFalse(self.arcade._Arcade__running)


if __name__ == '__main__':
    unittest.main()
