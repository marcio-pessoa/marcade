"""
---
name: test_m2048.py
description: Test M2048 Game
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock pygame before importing m2048
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.locals'] = MagicMock()

# Now we can import the game
from games.m2048 import M2048
from src.game_template import Game

class TestM2048(unittest.TestCase):
    """ Test M2048 Game """

    @patch('src.game_template.Game.__init__', autospec=True)
    def setUp(self, mock_game_init):
        # Mock Game.__init__ to set canvas
        def game_init_side_effect(instance, screen):
            instance.screen = screen
            instance.canvas = MagicMock()
            instance.screen_size = [800, 600]

        mock_game_init.side_effect = game_init_side_effect

        self.screen = MagicMock()
        self.game = M2048(self.screen)

        # Reset grid for testing
        self.game.grid = [[0] * 4 for _ in range(4)]
        self.game.score = 0
        self.game.animations = []
        self.game.animating = False

    def test_merge_simple(self):
        """ Test simple merge """
        line = [0, 2, 0, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [2, 0, 0, 0])
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0]['from'], 1)
        self.assertEqual(moves[0]['to'], 0)

    def test_merge_combine(self):
        """ Test merge combine """
        line = [2, 2, 0, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [4, 0, 0, 0])
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0]['to'], 0)
        self.assertEqual(moves[1]['to'], 0)
        self.assertTrue(moves[1]['merged'])

    def test_merge_move_and_combine(self):
        """ Test move and combine """
        line = [2, 0, 2, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [4, 0, 0, 0])
        self.assertEqual(len(moves), 2)

    def test_no_move(self):
        """ Test no move """
        line = [4, 2, 0, 0]
        new_line, moves = self.game._merge(line)
        self.assertEqual(new_line, [4, 2, 0, 0])

    def test_move_up(self):
        """ Test move up """
        self.game.grid = [
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        moved = self.game._move('UP')
        self.assertTrue(moved)
        self.assertEqual(self.game.grid[0][0], 2)
        self.assertEqual(self.game.grid[1][0], 0)
        self.assertTrue(len(self.game.animations) > 0)

    def test_check_game_over_false(self):
        """ Test game over false """
        self.game.grid = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 0] # One empty spot
        ]
        self.assertFalse(self.game._check_game_over())

    def test_check_game_over_true(self):
        """ Test game over true """
        self.game.grid = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2] # No moves possible
        ]
        self.assertTrue(self.game._check_game_over())

if __name__ == '__main__':
    unittest.main()
