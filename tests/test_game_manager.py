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
from src.game_manager import GameManager


class TestGameManager(unittest.TestCase):
    """ Test Game Manager """

    def test_get_games(self):
        """ Test get_games """
        game_manager = GameManager()
        games = game_manager.get_games()
        self.assertIsInstance(games, dict)
        self.assertGreater(len(games), 0)

    def test_get_game(self):
        """ Test get_game """
        game_manager = GameManager()
        game = game_manager.get_game('invasion')
        self.assertIsNotNone(game)
        game = game_manager.get_game('invalid_game')
        self.assertIsNone(game)


if __name__ == '__main__':
    unittest.main()
