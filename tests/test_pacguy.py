# pylint: disable=protected-access
"""
---
name: test_pacguy.py
description: Test Pac-Guy Game
people:
  developers:
  - name: Your Name
    email: your.email@example.com
"""
import unittest
from unittest.mock import MagicMock, patch
import sys


class TestPacGuy(unittest.TestCase):
    """ Test Pac-Guy Game """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()
        cls.mock_src_font = MagicMock()
        cls.mock_src_sound = MagicMock()
        cls.mock_src_timer = MagicMock()

        cls.modules_patcher = patch.dict(sys.modules, {
            'pygame': cls.mock_pygame,
            'pygame.locals': cls.mock_pygame.locals,
            'src.font': cls.mock_src_font,
            'src.sound': cls.mock_src_sound,
            'src.timer': cls.mock_src_timer
        })
        cls.modules_patcher.start()

        # Import modules AFTER patching
        # pylint: disable=import-outside-toplevel
        from games.pacguy import PacGuy
        cls.PacGuy = PacGuy

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        with patch('games.pacguy.Game.__init__'):
            self.game = self.PacGuy(self.screen)
            self.game.screen = self.screen
            self.game.start()  # Reset game state for each test

    def test_initialization(self):
        """ Test initialization """

        # Player starting position (default)
        self.assertEqual(getattr(self.game, "_PacGuy__player_pos"), [1, 1])
        # Ghosts starting position
        self.assertEqual(len(getattr(self.game, "_PacGuy__ghosts_pos")), 4)
        # Dots count
        self.assertEqual(len(getattr(self.game, "_PacGuy__dots")), 210)
        # Initial score
        self.assertEqual(getattr(self.game, "_PacGuy__score"), 0)
        # Player alive
        self.assertTrue(getattr(self.game, "_PacGuy__alive"))

    def test_player_movement(self):
        """ Test player movement on a valid path """

        # Set player to a known safe position
        setattr(self.game, "_PacGuy__player_pos", [1, 1])
        setattr(
            self.game, "_PacGuy__direction",
            getattr(self.game, "_PacGuy__down")
        )

        # Move down
        setattr(
            self.game, "_PacGuy__next_direction",
            getattr(self.game, "_PacGuy__down")
        )
        self.game._move_player()
        self.assertEqual(getattr(self.game, "_PacGuy__player_pos"), [1, 2])
        # Move right
        setattr(self.game, "_PacGuy__player_pos", [1, 3])
        setattr(
            self.game, "_PacGuy__next_direction",
            getattr(self.game, "_PacGuy__right")
        )
        self.game._move_player()
        self.assertEqual(getattr(self.game, "_PacGuy__player_pos"), [2, 3])
        # Move left
        setattr(
            self.game, "_PacGuy__next_direction",
            getattr(self.game, "_PacGuy__left")
        )
        self.game._move_player()
        self.assertEqual(getattr(self.game, "_PacGuy__player_pos"), [1, 3])
        # Move up
        setattr(
            self.game, "_PacGuy__next_direction",
            getattr(self.game, "_PacGuy__up")
        )
        self.game._move_player()
        self.assertEqual(getattr(self.game, "_PacGuy__player_pos"), [1, 2])

    def test_wall_collision(self):
        """ Test wall collision """
        # Player position at [1,1], trying to move UP into a wall at [1,0]
        setattr(self.game, "_PacGuy__player_pos", [1, 1])
        setattr(
            self.game, "_PacGuy__direction", getattr(self.game, "_PacGuy__up")
        )
        setattr(
            self.game, "_PacGuy__next_direction",
            getattr(self.game, "_PacGuy__up")
        )
        self.game._move_player()
        # Position should not change
        self.assertEqual(getattr(self.game, "_PacGuy__player_pos"), [1, 1])

        # Trying to move LEFT into a wall at [0,1]
        setattr(
            self.game, "_PacGuy__direction",
            getattr(self.game, "_PacGuy__left")
        )
        setattr(
            self.game, "_PacGuy__next_direction",
            getattr(self.game, "_PacGuy__left")
        )
        self.game._move_player()
        # Position should not change
        self.assertEqual(getattr(self.game, "_PacGuy__player_pos"), [1, 1])

    def test_dot_collision(self):
        """ Test dot collision """

        # Manually place a dot and player
        setattr(self.game, "_PacGuy__dots", [(1, 3)])
        setattr(self.game, "_PacGuy__player_pos", [1, 3])
        initial_score = getattr(self.game, "_PacGuy__score")
        self.game._check_collisions()
        self.assertEqual(
            getattr(self.game, "_PacGuy__score"), initial_score + 10
        )
        self.assertEqual(len(getattr(self.game, "_PacGuy__dots")), 0)

    def test_ghost_collision(self):
        """ Test ghost collision """

        setattr(self.game, "_PacGuy__player_pos", [10, 9])
        setattr(self.game, "_PacGuy__ghosts_pos", [[10, 9]])
        self.game._check_collisions()
        self.assertFalse(getattr(self.game, "_PacGuy__alive"))


if __name__ == '__main__':
    unittest.main()
