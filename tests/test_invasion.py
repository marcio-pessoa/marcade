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

# Mock pygame before importing invasion
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.locals'] = MagicMock()

# Mock src modules that invasion imports
sys.modules['src.font'] = MagicMock()
sys.modules['src.sound'] = MagicMock()
sys.modules['src.timer'] = MagicMock()
sys.modules['src.game_template'] = MagicMock()

from games.invasion import Ship, Missile, Monster, Barrier, Invasion

class TestShip(unittest.TestCase):
    """ Test Ship Class """

    def setUp(self):
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        self.ship = Ship(self.screen)
        # Reset position to known value for testing
        self.ship.position = [400, 500]

    def test_initialization(self):
        self.assertTrue(self.ship.enable)
        self.assertIsNotNone(self.ship.shape)

    def test_move_right(self):
        initial_x = self.ship.position[0]
        self.ship.move_right()
        self.assertEqual(self.ship.position[0], initial_x + 5)

    def test_move_left(self):
        initial_x = self.ship.position[0]
        self.ship.move_left()
        self.assertEqual(self.ship.position[0], initial_x - 5)

    def test_boundary_left(self):
        self.ship.position[0] = -10
        self.ship.update()
        self.assertEqual(self.ship.position[0], 0)

    def test_boundary_right(self):
        # Ship width is 48
        screen_width = 800
        self.ship.position[0] = 850
        self.ship.update()
        self.assertEqual(self.ship.position[0], screen_width - 48)

class TestMissile(unittest.TestCase):
    """ Test Missile Class """

    def setUp(self):
        self.screen = MagicMock()
        # ship_pos, speed, direction
        self.missile = Missile(self.screen, [100, 100], 10, 1)

    def test_initialization(self):
        self.assertTrue(self.missile.enable)
        self.assertFalse(self.missile.out)
        self.assertEqual(self.missile.speed, 10)

    def test_update_move(self):
        initial_y = self.missile.position[1]
        self.missile.update()
        # Moving up (direction 1) means y decreases
        self.assertEqual(self.missile.position[1], initial_y - 10)

    def test_out_of_bounds(self):
        self.missile.position[1] = -5
        self.missile.update()
        self.assertTrue(self.missile.out)

class TestMonster(unittest.TestCase):
    """ Test Monster Class """

    def setUp(self):
        self.screen = MagicMock()
        # aspect 0
        self.monster = Monster(self.screen, 0, [0, 0])

    def test_points(self):
        # aspect 0 -> 10 points
        self.assertEqual(self.monster.points, 10)

        monster2 = Monster(self.screen, 1, [0, 0])
        self.assertEqual(monster2.points, 9)

    def test_march(self):
        initial_x = self.monster.position[0]
        self.monster.march(True, False) # Right, no drop
        self.assertEqual(self.monster.position[0], initial_x + 4)

        self.monster.march(False, True) # Left, drop
        self.assertEqual(self.monster.position[0], initial_x + 4 - 4) # Back to start
        self.assertEqual(self.monster.position[1], 16) # Dropped 16

class TestBarrier(unittest.TestCase):
    """ Test Barrier Class """

    def setUp(self):
        self.screen = MagicMock()
        self.barrier = Barrier(self.screen, [0, 0])

    def test_add_damage(self):
        initial_status = self.barrier.status
        new_status = self.barrier.add_damage()
        self.assertEqual(new_status, initial_status - 1)

if __name__ == '__main__':
    unittest.main()
