"""
---
name: serpent.py
description: Serpent game package file
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  designers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  - name: Gus
  beta-testers:
  - name: Nicolas Masaishi Oi Pessoa
    email: masaishi.pessoa@gmail.com
"""

import sys
import random
import pygame
try:
    from pygame.locals import K_RETURN, K_ESCAPE, K_UP, K_RIGHT, K_DOWN, K_LEFT
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)

from tools.log import log
from tools.font import Font
from tools.game_template import Game
from tools.sound import Sound
from tools.timer import Timer


class Serpent(Game):
    """ Serpent game class """

    __version__ = '0.1.0'
    __up = 0
    __right = 1
    __down = 2
    __left = 3
    __matrix = (50, 30)

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.__fruit_position: tuple[int]
        self.__direction: int
        self.__serpent: list
        self.__alive: bool
        self.__score: int
        self.__sound = Sound()
        self.__update = Timer(150)
        self.start()

    def start(self) -> None:
        self.__fruit_position = self._random_position()
        self.__direction = self.__left
        self.__serpent = [(23, 15), (24, 15), (25, 15)]
        self.__score = 0
        self.__alive = True

    def reset(self) -> None:
        self.start()

    def update(self) -> None:
        if not self.__update.check():
            return

        if self.__alive:
            self._check_collision()

        self._draw_grid()
        self._fruit_update()
        self._serpent_update()

        if self.__alive:
            self._serpent_move()
        else:
            self._game_over()

    def control(self, keys, joystick) -> None:
        if joystick:
            if joystick['hat'][0]['x'] < 0 or \
               joystick['axis'][0] < 0:
                self.__direction = self.__left
            if joystick['hat'][0]['x'] > 0 or \
               joystick['axis'][0] > 0:
                self.__direction = self.__right
            if joystick['hat'][0]['y'] > 0 or \
               joystick['axis'][1] > 0:
                self.__direction = self.__up
            if joystick['hat'][0]['y'] < 0 or \
               joystick['axis'][1] < 0:
                self.__direction = self.__down
        if K_ESCAPE in keys:
            self.stop()
        if K_RETURN in keys:
            self.reset()
        if K_UP in keys and self.__direction != self.__down:
            self.__direction = self.__up
        if K_RIGHT in keys and self.__direction != self.__left:
            self.__direction = self.__right
        if K_DOWN in keys and self.__direction != self.__up:
            self.__direction = self.__down
        if K_LEFT in keys and self.__direction != self.__right:
            self.__direction = self.__left

    def _check_collision(self):
        # Collision with fruit
        if self.__fruit_position in self.__serpent:
            self._serpent_grow()
            self._spawn_fruit()
            self.__score += 1
            self.__sound.tone(600)

        # Collision with boundaries
        if self.__serpent[0][0] < 0 or \
           self.__serpent[0][0] >= self.__matrix[0] or \
           self.__serpent[0][1] < 0 or \
           self.__serpent[0][1] >= self.__matrix[1]:
            self.__alive = False
            self.__sound.tone(800)

        # Collision with itself
        if self.__serpent.count(self.__serpent[0]) > 1:
            self.__alive = False
            self.__sound.tone(200)

    def _serpent_move(self):
        for i in range(len(self.__serpent) - 1, 0, -1):
            self.__serpent[i] = (
                self.__serpent[i-1][0],
                self.__serpent[i-1][1]
            )

        if self.__direction == self.__up:
            self.__serpent[0] = (
                self.__serpent[0][0],
                self.__serpent[0][1] - 1
            )
        if self.__direction == self.__right:
            self.__serpent[0] = (
                self.__serpent[0][0] + 1,
                self.__serpent[0][1]
            )
        if self.__direction == self.__down:
            self.__serpent[0] = (
                self.__serpent[0][0],
                self.__serpent[0][1] + 1
            )
        if self.__direction == self.__left:
            self.__serpent[0] = (
                self.__serpent[0][0] - 1,
                self.__serpent[0][1]
            )

    def _serpent_grow(self):
        self.__serpent.append(self.__serpent[-1])

    def _serpent_update(self):
        for i in self.__serpent:
            coordinate = self._position(i, 0.6)
            bud = pygame.Surface((15, 15))
            bud.fill((64, 192, 64))
            self.screen.blit(bud, coordinate)

    def _spawn_fruit(self):
        self.__fruit_position = self._random_position()
        log.debug('Spawning fruit on: %s', self.__fruit_position)

    def _fruit_update(self,):
        coordinate = self._position(self.__fruit_position, 2.6)
        fruit = pygame.Surface((11, 11))
        fruit.fill((192, 0, 0))
        self.screen.blit(fruit, coordinate)

    def _game_over(self):
        message = Font(self.screen)
        message.size = 9
        message.position = [161, 120]
        message.color = (96, 5, 5)
        message.echo("GAME OVER")
        score = Font(self.screen)
        score.size = 9
        score.position = [186, 300]
        score.color = (96, 5, 5)
        score.echo(f'SCORE {self.__score}')

    def _position(self, position: int, padding: int = 0) -> list[int]:
        return (
            self.screen.get_size()[0] / self.__matrix[0] * position[0] +
            padding,
            self.screen.get_size()[1] / self.__matrix[1] * position[1] +
            padding
        )

    def _random_position(self):
        return (
            random.randint(1, self.__matrix[0]),
            random.randint(1, self.__matrix[1])
        )

    def _draw_grid(self):
        self.screen.fill((0, 0, 0))
        color = (60, 60, 60)
        for i in range(self.__matrix[0] + 1):
            x_axis = (self.screen.get_size()[0] - 1) / self.__matrix[0] * i
            pygame.draw.line(
                surface=self.screen,
                color=color,
                start_pos=(x_axis, 0),
                end_pos=(x_axis, self.screen.get_size()[1]),
                width=1
            )
        for i in range(self.__matrix[1] + 1):
            y_axis = (self.screen.get_size()[1] - 1) / self.__matrix[1] * i
            pygame.draw.line(
                surface=self.screen,
                color=color,
                start_pos=(0, y_axis),
                end_pos=(self.screen.get_size()[0], y_axis),
                width=1
            )
