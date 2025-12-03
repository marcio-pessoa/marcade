"""
---
name: test_font.py
description: Test Font Class
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys


class TestFont(unittest.TestCase):
    """ Test Font Class """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()

        cls.modules_patcher = patch.dict(sys.modules, {
            'pygame': cls.mock_pygame,
            'pygame.locals': cls.mock_pygame.locals,
        })
        cls.modules_patcher.start()

        # pylint: disable=import-outside-toplevel
        from src.font import Font
        cls.Font = Font

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.pygame_patcher = patch('src.font.pygame')
        self.mock_pygame = self.pygame_patcher.start()
        self.screen = MagicMock()
        self.font = self.Font(self.screen)

    def tearDown(self):
        """ Tear down test """
        self.pygame_patcher.stop()

    def test_initialization(self):
        """ Test initialization """
        self.assertEqual(self.font.size, 1)
        self.assertEqual(self.font.position, [0, 0])
        self.assertEqual(self.font.color, [200, 200, 200])

    def test_echo(self):
        """ Test echo """
        self.font.echo("A")
        self.screen.blit.assert_called_once()
        self.mock_pygame.draw.rect.assert_called()


if __name__ == '__main__':
    unittest.main()
