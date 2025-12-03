"""
---
name: test_serpent.py
description: Test Serpent Game
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys


class TestSerpent(unittest.TestCase):
    """ Test Serpent Game """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()
        cls.mock_font = MagicMock()
        cls.mock_sound = MagicMock()
        cls.mock_timer = MagicMock()

        cls.modules_patcher = patch.dict(sys.modules, {
            'pygame': cls.mock_pygame,
            'pygame.locals': cls.mock_pygame.locals,
            'src.font': cls.mock_font,
            'src.sound': cls.mock_sound,
            'src.timer': cls.mock_timer,
        })
        cls.modules_patcher.start()

        # pylint: disable=import-outside-toplevel
        from games.serpent import Serpent
        cls.Serpent = Serpent

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        self.game = self.Serpent(self.screen)

    def test_initialization(self):
        """ Test initialization """
        self.assertEqual(len(self.game._Serpent__serpent), 3)
        self.assertTrue(self.game._Serpent__alive)

    def test_serpent_move(self):
        """ Test serpent movement """
        initial_head = self.game._Serpent__serpent[0]
        self.game._Serpent__direction = self.game._Serpent__up
        self.game._serpent_move()
        new_head = self.game._Serpent__serpent[0]
        self.assertEqual(new_head, (initial_head[0], initial_head[1] - 1))

    def test_serpent_grow(self):
        """ Test serpent growth """
        initial_length = len(self.game._Serpent__serpent)
        self.game._serpent_grow()
        self.assertEqual(len(self.game._Serpent__serpent), initial_length + 1)

    def test_collision_with_fruit(self):
        """ Test collision with fruit """
        self.game._Serpent__serpent = [(20, 15), (21, 15), (22, 15)]
        self.game._Serpent__fruit_position = (20, 15)
        initial_score = self.game._Serpent__score
        self.game._check_collision()
        self.assertEqual(self.game._Serpent__score, initial_score + 1)

    def test_collision_with_wall(self):
        """ Test collision with wall """
        self.game._Serpent__serpent = [(-1, 15), (0, 15), (1, 15)]
        self.game._check_collision()
        self.assertFalse(self.game._Serpent__alive)


if __name__ == '__main__':
    unittest.main()
