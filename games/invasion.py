"""
---
name: invasion.py
description: Invasion package file
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  designers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  - name: Nicolas Masaishi Oi Pessoa
    email: masaishi.pessoa@gmail.com
  - name: Gus
"""

import sys
import random
import pygame
try:
    from pygame.locals import (SRCALPHA, K_ESCAPE, K_RIGHT, K_LEFT, K_SPACE,
                               K_a, K_RETURN)
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)

from src.font import Font
from src.sound import Sound
from src.timer import Timer
from src.game_template import Game
from games.actor import Ship, Missile, Monster, Barrier, Explosion


class Invasion(Game):  # pylint: disable=too-many-instance-attributes
    """ Invasion game class """

    __version__ = '0.5.3'

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.ship_burst = set()
        self.alien_burst = set()
        self.walls = set()
        self.aliens = set()
        self.explosions = set()
        self.ship = Ship(self.canvas)
        self.lives = 0

        self.start_march_period = 600
        self.shoot_timer = Timer(50)
        self.march_timer = Timer(self.start_march_period)

        self.scoreboard = Font(self.canvas)
        self.scoreboard.size = 3
        self.scoreboard.position = [10, 5]

        self.livesboard = Font(self.canvas)
        self.livesboard.size = 3
        self.livesboard.position = [330, 5]

        self.levelboard = Font(self.canvas)
        self.levelboard.size = 3
        self.levelboard.position = [580, 5]

        self.alien_burst_seed = 2000
        self.way = True
        self.drop = False
        self.sound = Sound()
        self.reset()

    def start(self):
        self.ship_burst = set()
        self.alien_burst = set()
        self.walls = set()
        self.aliens = set()
        self.explosions = set()
        self.alien_burst_seed = 2000
        self.march_timer.period = self.start_march_period
        self.way = True
        self.drop = False
        self.ship.reset()
        self._walls_deploy()
        self._aliens_deploy()

    def reset(self):
        self.level = 0
        self.lives = 2
        self.score = 0
        self.start_march_period = 600
        self.start()
        self._level_up()

    def update(self):
        self.canvas.fill([0, 0, 0])  # Black
        self._score_update()
        self._burst_update()
        self._walls_update()
        self.ship.update()
        self._aliens_update()
        self._explosions_update()
        self._collision_check()
        self._aliens_check()
        self._lives_check()
        self.screen.blit(self.canvas, [0, 0])
        return False

    def control(self, keys, joystick):
        if joystick:
            if joystick['hat'][0]['x'] < 0 or \
               joystick['axis'][0] < 0:
                self.ship.move_left()
            if joystick['hat'][0]['x'] > 0 or \
               joystick['axis'][0] > 0:
                self.ship.move_right()
            if joystick['button'][10]:
                self.reset()
            if joystick['button'][0] or joystick['button'][7]:
                self._ship_shoot()
        if K_ESCAPE in keys:
            self.stop()
        if K_RIGHT in keys:
            self.ship.move_right()
        if K_LEFT in keys:
            self.ship.move_left()
        if K_SPACE in keys or K_a in keys:
            self._ship_shoot()
        if K_RETURN in keys:
            self.reset()

    def _lives_check(self):
        if self.lives == 0:
            self.game_over()

    def _collision_check(self):  # pylint: disable=too-many-branches
        # Ship Missile against Alien
        for i in self.aliens:
            for j in self.ship_burst:
                if i.rect.colliderect(j.rect):
                    explosion = Explosion(self.canvas, i.position)
                    self.explosions.add(explosion)
                    self.score += i.points
                    self.aliens.remove(i)
                    self.ship_burst.remove(j)
                    self.sound.tone(400)
                    return
        # Ship Missile against Wall
        for i in self.walls:
            for j in self.ship_burst:
                if i.rect.colliderect(j.rect):
                    self.score += i.points
                    if i.add_damage() <= 0:
                        self.walls.remove(i)
                    self.ship_burst.remove(j)
                    self.sound.tone(200)
                    return
        # Alien Missile against Wall
        for i in self.walls:
            for j in self.alien_burst:
                if i.rect.colliderect(j.rect):
                    if i.add_damage() <= 0:
                        self.walls.remove(i)
                    self.alien_burst.remove(j)
                    self.sound.tone(200)
                    return
        # Alien against Wall
        for i in self.aliens:
            for j in self.walls:
                if i.rect.colliderect(j.rect):
                    explosion = Explosion(self.canvas, i.position)
                    self.explosions.add(explosion)
                    explosion = Explosion(self.canvas, j.position)
                    self.explosions.add(explosion)
                    self.aliens.remove(i)
                    self.walls.remove(j)
                    self.sound.tone(200)
                    return
        # Ship against Alien
        for i in self.aliens:
            if i.rect.colliderect(self.ship.rect):
                explosion = Explosion(self.canvas, i.position)
                self.explosions.add(explosion)
                explosion = Explosion(self.canvas, self.ship.position)
                self.explosions.add(explosion)
                self.aliens.remove(i)
                self.lives -= 1
                self.sound.tone(200)
                return
        # Alien Missile against Ship
        for i in self.alien_burst:
            if i.rect.colliderect(self.ship.rect):
                explosion = Explosion(self.canvas, self.ship.position)
                self.explosions.add(explosion)
                self.alien_burst.remove(i)
                self.lives -= 1
                self.sound.tone(200)
                return

    def _burst_update(self):
        # Update position
        for i in self.ship_burst:
            i.update()
        for i in self.alien_burst:
            i.update()
        # Check shoot age
        for i in self.ship_burst:
            if i.out:
                self.ship_burst.remove(i)
                break

    def _aliens_deploy(self):
        formation = (7, 6)
        for cartesian_y in range(formation[1]):
            for cartesian_x in range(formation[0]):
                monster = Monster(
                    self.canvas,
                    cartesian_y,
                    [
                        (
                            self.screen_size[0] / formation[0]
                        ) * cartesian_x + (
                            self.screen_size[0] / formation[0]
                        ) / 3,
                        (
                            (self.screen_size[1] /
                             (formation[1] + 3) * cartesian_y)
                        ) + 30
                    ]
                )
                self.aliens.add(monster)

    def _aliens_update(self):
        # Update
        for i in self.aliens:
            i.update()
        if self.lives == 0:
            return
        if self.march_timer.check():
            self.sound.tone(600)
            # Aliens lateral boundaries
            for i in self.aliens:
                if not self.canvas.get_rect().contains(i.rect):
                    self.way = not self.way
                    if self.way:
                        self.drop = True
                        self.march_timer.period /= 1.15
                    break
            # Aliens fall down
            for i in self.aliens:
                i.march(self.way, self.drop)
            self.drop = False
        # Aliens landing
        for i in self.aliens:
            if i.position[1] + i.size[1] >= self.screen_size[1]:
                self.lives = 0
                break
        # Fire
        for i in self.aliens:
            if random.randrange(self.alien_burst_seed) == 1:
                shoot = Missile(self.canvas, i.position, 4, -1)
                self.alien_burst.add(shoot)
                break

    def game_over(self):
        self.ship.enable = False
        for i in self.aliens:
            i.enable = False
        for i in self.ship_burst:
            i.enable = False
        for i in self.alien_burst:
            i.enable = False
        message = Font(self.canvas)
        message.size = 9
        message.position = [180, 60]
        message.color = (96, 5, 5)
        message.echo("GAME OVER")
        return super().game_over()

    def _aliens_check(self):
        if len(self.aliens) == 0:
            self._level_up()

    def _level_up(self):
        self.level += 1
        self.lives += 1
        self.alien_burst_seed -= self.level * 100
        self.start_march_period -= self.start_march_period * self.level / 20
        self.start()

    def _walls_deploy(self):
        quantity = 4
        for i in range(quantity):
            position = (self.screen.get_size()[0] / quantity * i +
                        (self.screen.get_size()[0] / quantity / 2 - 24), 400)
            barrier = Barrier(self.canvas, position)
            self.walls.add(barrier)

    def _walls_update(self):
        for i in self.walls:
            i.update()

    def _score_update(self):
        self.scoreboard.echo(str(self.score))
        self.livesboard.echo(str(self.lives))
        self.levelboard.echo(str(self.level))

    def _explosions_update(self):
        for i in self.explosions:
            i.update()
            if i.done:
                self.explosions.remove(i)
                return

    def _ship_shoot(self):
        # Limit shoot frequency
        if not self.shoot_timer.check():
            return
        # Limit burst size
        if len(self.ship_burst) >= 1:
            return
        # Shoot!
        shoot = Missile(self.canvas, self.ship.position, 5)
        self.ship_burst.add(shoot)
        self.sound.tone(1200)


