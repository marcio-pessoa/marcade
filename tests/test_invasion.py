"""
---
name: test_invasion.py
description: Test Invasion Game
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import MagicMock, patch
import sys


class TestInvasion(unittest.TestCase):
    """ Test Invasion Game """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        # Create mocks
        cls.mock_pygame = MagicMock()
        cls.mock_pygame.locals = MagicMock()
        cls.mock_src_font = MagicMock()
        cls.mock_src_sound = MagicMock()
        cls.mock_src_timer = MagicMock()
        cls.mock_src_game_template = MagicMock()

        # Apply patches
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
        from games.invasion import (
            Ship, Missile, Monster, Barrier, Invasion
        )
        cls.Ship = Ship
        cls.Missile = Missile
        cls.Monster = Monster
        cls.Barrier = Barrier
        cls.Invasion = Invasion

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()


class TestShip(TestInvasion):
    """ Test Ship Class """

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        self.ship = self.Ship(self.screen)
        # Reset position to known value for testing
        self.ship.position = [400, 500]

    def test_initialization(self):
        """ Test initialization """
        self.assertTrue(self.ship.enable)
        self.assertIsNotNone(self.ship.shape)

    def test_move_right(self):
        """ Test move right """
        initial_x = self.ship.position[0]
        self.ship.move_right()
        self.assertEqual(self.ship.position[0], initial_x + 5)

    def test_move_left(self):
        """ Test move left """
        initial_x = self.ship.position[0]
        self.ship.move_left()
        self.assertEqual(self.ship.position[0], initial_x - 5)

    def test_boundary_left(self):
        """ Test left boundary """
        self.ship.position[0] = -10
        self.ship.update()
        self.assertEqual(self.ship.position[0], 0)

    def test_boundary_right(self):
        """ Test right boundary """
        # Ship width is 48
        screen_width = 800
        self.ship.position[0] = 850
        self.ship.update()
        self.assertEqual(self.ship.position[0], screen_width - 48)


class TestMissile(TestInvasion):
    """ Test Missile Class """

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        # ship_pos, speed, direction
        self.missile = self.Missile(self.screen, [100, 100], 10, 1)

    def test_initialization(self):
        """ Test initialization """
        self.assertTrue(self.missile.enable)
        self.assertFalse(self.missile.out)
        self.assertEqual(self.missile.speed, 10)

    def test_update_move(self):
        """ Test update move """
        initial_y = self.missile.position[1]
        self.missile.update()
        # Moving up (direction 1) means y decreases
        self.assertEqual(self.missile.position[1], initial_y - 10)

    def test_out_of_bounds(self):
        """ Test out of bounds """
        self.missile.position[1] = -5
        self.missile.update()
        self.assertTrue(self.missile.out)


class TestMonster(TestInvasion):
    """ Test Monster Class """

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        # aspect 0
        self.monster = self.Monster(self.screen, 0, [0, 0])

    def test_points(self):
        """ Test points """
        # aspect 0 -> 10 points
        self.assertEqual(self.monster.points, 10)

        monster2 = self.Monster(self.screen, 1, [0, 0])
        self.assertEqual(monster2.points, 9)

    def test_march(self):
        """ Test march """
        initial_x = self.monster.position[0]
        self.monster.march(True, False)  # Right, no drop
        self.assertEqual(self.monster.position[0], initial_x + 4)

        self.monster.march(False, True)  # Left, drop
        # Back to start
        self.assertEqual(self.monster.position[0], initial_x + 4 - 4)
        self.assertEqual(self.monster.position[1], 16)  # Dropped 16


class TestBarrier(TestInvasion):
    """ Test Barrier Class """

    def setUp(self):
        """ Set up test """
        self.screen = MagicMock()
        self.barrier = self.Barrier(self.screen, [0, 0])

    def test_add_damage(self):
        """ Test add damage """
        initial_status = self.barrier.status
        new_status = self.barrier.add_damage()
        self.assertEqual(new_status, initial_status - 1)


if __name__ == '__main__':
    unittest.main()
