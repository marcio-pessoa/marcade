"""
---
name: test_game_manager.py
description: Test Game Manager package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""
import unittest
from unittest.mock import MagicMock, patch
import sys


class TestGameManager(unittest.TestCase):
    """ Test Game Manager """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()
        cls.mock_src_font = MagicMock()
        cls.mock_src_sound = MagicMock()
        cls.mock_src_timer = MagicMock()
        cls.mock_src_game_template = MagicMock()

        cls.modules_patcher = patch.dict(sys.modules, {
            'pygame': cls.mock_pygame,
            'pygame.locals': cls.mock_pygame.locals,
            'src.font': cls.mock_src_font,
            'src.sound': cls.mock_src_sound,
            'src.timer': cls.mock_src_timer,
            'src.game_template': cls.mock_src_game_template
        })
        cls.modules_patcher.start()

        # Import modules AFTER patching
        # pylint: disable=import-outside-toplevel
        from src.game_manager import GameManager
        cls.GameManager = GameManager

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def test_get_games(self):
        """ Test get_games """
        game_manager = self.GameManager()
        games = game_manager.get_games()
        self.assertIsInstance(games, dict)
        self.assertGreater(len(games), 0)

    def test_get_game(self):
        """ Test get_game """
        game_manager = self.GameManager()
        game = game_manager.get_game('invasion')
        self.assertIsNotNone(game)
        game = game_manager.get_game('invalid_game')
        self.assertIsNone(game)


if __name__ == '__main__':
    unittest.main()
