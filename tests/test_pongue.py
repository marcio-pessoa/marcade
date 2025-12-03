"""
---
name: test_pongue.py
description: Test Pongue Game
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import pygame


class TestPongue(unittest.TestCase):
    """ Test Pongue Game """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()
        cls.mock_font = MagicMock()
        cls.mock_sound = MagicMock()

        cls.modules_patcher = patch.dict(sys.modules, {
            'pygame': cls.mock_pygame,
            'pygame.locals': cls.mock_pygame.locals,
            'src.font': cls.mock_font,
            'src.sound': cls.mock_sound,
        })
        cls.modules_patcher.start()

        # pylint: disable=import-outside-toplevel
        from games.pongue import Pongue
        cls.Pongue = Pongue

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        with patch('pygame.Surface') as mock_surface:
            mock_canvas = MagicMock()
            mock_canvas.get_size.return_value = (800, 600)
            mock_canvas.convert_alpha.return_value = None
            mock_play_area = MagicMock()
            mock_play_area.get_size.return_value = (798, 598)
            mock_play_area.convert_alpha.return_value = None
            mock_surface.side_effect = [mock_canvas, mock_play_area]
            self.game = self.Pongue(self.screen)

    def test_initialization(self):
        """ Test initialization """
        self.assertIsInstance(self.game, self.Pongue)
        self.assertEqual(self.game.score, [0, 0])

    def test_ball_spawn(self):
        """ Test ball spawn """
        self.game._ball_spawn()  # pylint: disable=protected-access
        self.assertNotEqual(self.game.ball_velocity[0], 0)
        self.assertNotEqual(self.game.ball_velocity[1], 0)

    def test_pad1_movement(self):
        """ Test pad1 movement """
        initial_pos = self.game.pad1_position
        self.game.pad1_vel = 5
        self.game._draw_pad1()  # pylint: disable=protected-access
        self.assertEqual(self.game.pad1_position, initial_pos + 5)

    def test_pad2_movement(self):
        """ Test pad2 movement """
        initial_pos = self.game.pad2_position
        self.game.pad2_vel = -5
        self.game._draw_pad2()  # pylint: disable=protected-access
        self.assertEqual(self.game.pad2_position, initial_pos - 5)

    def test_ball_wall_collision(self):
        """ Test ball wall collision """
        self.game.ball_position = [400, 10]
        self.game.ball_velocity = [2, -2]
        self.game.ball_radius = 15
        self.game._ball_check()  # pylint: disable=protected-access
        self.assertEqual(self.game.ball_velocity[1], 2)

    def test_player1_scores(self):
        """ Test player 1 scores """
        self.game.ball_position = [
            self.game.play_area.get_size()[0] - self.game.pad_width + 10,
            300
        ]
        self.game.ball_velocity = [2, 2]
        self.game.pad2_position = 500
        self.game.pad_height_half = 50
        initial_score = self.game.score[0]
        self.game._ball_check()  # pylint: disable=protected-access
        self.assertEqual(self.game.score[0], initial_score + 1)

    def test_player2_scores(self):
        """ Test player 2 scores """
        self.game.ball_position = [self.game.pad_width - 10, 300]
        self.game.ball_velocity = [-2, 2]
        self.game.pad1_position = 500
        self.game.pad_height_half = 50
        initial_score = self.game.score[1]
        self.game._ball_check()  # pylint: disable=protected-access
        self.assertEqual(self.game.score[1], initial_score + 1)


if __name__ == '__main__':
    unittest.main()
