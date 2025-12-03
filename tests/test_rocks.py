"""
---
name: test_rocks.py
description: Test Rocks Game
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import math


class TestRocks(unittest.TestCase):
    """ Test Rocks Game """
    # pylint: disable=protected-access, invalid-name

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
        from games.rocks import Rocks, Ship, Missile, Sprite
        cls.Rocks = Rocks
        cls.Ship = Ship
        cls.Missile = Missile
        cls.Sprite = Sprite

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)

        # Mock time for Missile
        self.mock_pygame.time.get_ticks.return_value = 0

        self.surface_patcher = patch('pygame.Surface', MagicMock())
        mock_surface_class = self.surface_patcher.start()

        mock_surface_instance = MagicMock()
        mock_surface_instance.get_size.return_value = (50, 50)
        mock_rect = MagicMock()
        mock_rect.center = (25, 25)
        mock_rect.copy.return_value = mock_rect
        mock_rect.move.return_value = mock_rect
        mock_surface_instance.get_rect.return_value = mock_rect
        mock_surface_class.return_value = mock_surface_instance

        # We need a ship to create a missile.
        ship_for_missile = self.Ship(self.screen)
        ship_for_missile.get_angle = MagicMock(return_value=0)
        ship_for_missile.get_position = MagicMock(return_value=[400, 300])
        ship_for_missile.get_radius = MagicMock(return_value=24)
        ship_for_missile.get_speed = MagicMock(return_value=[0, 0])

        self.game = self.Rocks(self.screen)
        self.ship = self.Ship(self.screen)
        self.ship.start()
        self.missile = self.Missile(self.screen, ship_for_missile)
        self.ship.start()
        self.missile = self.Missile(self.screen, ship_for_missile)
        self.sprite = self.Sprite(self.screen)

        self.mock_missile = MagicMock()
        self.mock_missile.update = MagicMock()
        self.mock_missile.age.return_value = 0

    def tearDown(self):
        """ Tear down test """
        self.surface_patcher.stop()
        self.mock_pygame.reset_mock()

    def test_ship_initialization(self):
        """ Test ship initialization """
        self.assertEqual(self.ship.position, [400, 300])
        self.assertEqual(self.ship.speed, [0, 0])
        self.assertEqual(self.ship.angle, math.pi / -2)

    def test_ship_thrust(self):
        """ Test ship thrust """
        self.ship.thrust_on()
        self.ship.update()
        # With angle = -pi/2 and thrust, acceleration is in direction [0, -1]
        self.assertAlmostEqual(self.ship.speed[0], 0)
        self.assertLess(self.ship.speed[1], 0)

    def test_missile_update(self):
        """ Test missile update """
        self.game.burst.add(self.mock_missile)
        self.game.burst_update()
        self.mock_missile.update.assert_called_once()
        self.assertIsNotNone(self.missile.position)
        self.assertIsNotNone(self.missile.speed)

    def test_rock_initialization(self):
        """ Test rock initialization """
        self.assertIsNotNone(self.sprite.position)
        self.assertIsNotNone(self.sprite.speed)

    def test_collision(self):
        """ Test collision """
        # Create a mock rect that will report a collision
        mock_colliding_rect = MagicMock()
        mock_colliding_rect.colliderect.return_value = True

        # Assign this rect to the ship and a rock
        self.game.ship.rect = mock_colliding_rect
        rock = self.Sprite(self.screen)
        rock.rect = mock_colliding_rect

        # Add the rock to the game's rock_group
        self.game.rock_group = {rock}

        # Check collision and assert lives decrease
        initial_lives = self.game.lives
        self.game.check_collision()
        self.assertEqual(self.game.lives, initial_lives - 1)


if __name__ == '__main__':
    unittest.main()
