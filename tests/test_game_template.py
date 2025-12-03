"""
---
name: test_game_template.py
description: Test Game Template Class
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys


class TestGameTemplate(unittest.TestCase):
    """ Test Game Template Class """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()
        cls.mock_log = MagicMock()

        cls.modules_patcher = patch.dict(sys.modules, {
            'pygame': cls.mock_pygame,
            'pygame.locals': cls.mock_pygame.locals,
            'src.log': cls.mock_log,
        })
        cls.modules_patcher.start()

        # pylint: disable=import-outside-toplevel
        from src.game_template import Game
        cls.Game = Game

        # Create a concrete implementation of the abstract class for testing
        class ConcreteGame(cls.Game):
            def control(self, keys, joystick):
                pass
            def update(self):
                pass
            def start(self):
                pass
            def game_over(self):
                pass
            def reset(self):
                pass
        cls.ConcreteGame = ConcreteGame

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        self.game = self.ConcreteGame(self.screen)

    def test_initialization(self):
        """ Test initialization """
        self.assertEqual(self.game.screen_size, [800, 600])
        self.mock_pygame.Surface.assert_called_with(
            [800, 600], self.mock_pygame.locals.SRCALPHA, 32)
        self.game.canvas.convert_alpha.assert_called_once()

    def test_stop(self):
        """ Test stop method """
        self.game.stop()
        self.mock_pygame.event.clear.assert_called_once()


if __name__ == '__main__':
    unittest.main()
