"""
---
name: pongue.py
description: Pongue game package file
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  designers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  beta-testers:
  - name: Nicolas Masaishi Oi Pessoa
    email: masaishi.pessoa@gmail.com
  - name: Gus
"""

import sys
import random
import pygame
try:
    from pygame.locals import K_ESCAPE, SRCALPHA, K_w, K_s, K_UP, K_DOWN
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)

from src.font import Font
from src.sound import Sound
from src.game_template import Game


class Pongue(Game):  # pylint: disable=too-many-instance-attributes
    """ Pongue game class """

    __version__ = '0.6.4'

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.pad1_position = [0, 0]
        self.pad2_position = [0, 0]
        self.pad1_vel = 0
        self.pad2_vel = 0
        self.ball_velocity = [0, 0]
        self.pad1_pressed = False
        self.pad2_pressed = False
        self.ball_position = [0, 0]
        self.score = [0, 0]
        self.ball_radius = 0
        self.pad_width = 0
        self.pad_height = 0
        self.pad_height_half = 0
        self.sound = Sound()
        self.court_side = 1
        self.pad_acceleration = 1
        self.delta_increment = 6
        self.play_area = 0
        self.score_player1 = 0
        self.score_player2 = 0
        self._size_set()
        self.pad_acceleration = 1
        self.delta_increment = 6
        self.court_side = 1
        self.reset()
        self.start()
        self._ball_spawn()

        self.score_player1 = Font(self.play_area)
        self.score_player1.size = 5
        self.score_player1.position = [290, 20]
        self.score_player1.color = (120, 120, 120)

        self.score_player2 = Font(self.play_area)
        self.score_player2.size = 5
        self.score_player2.position = [480, 20]
        self.score_player2.color = (120, 120, 120)

    def _size_set(self):
        self.play_area = pygame.Surface(
            [self.canvas.get_size()[0] - 2, self.canvas.get_size()[1] - 2],
            SRCALPHA,
            32,
        )
        self.play_area.convert_alpha()
        self.ball_radius = int(self.play_area.get_size()[0] * 0.03 / 2)
        self.pad_height_half = int(self.play_area.get_size()[1] * 0.2 / 2)
        self.pad_width = int(self.play_area.get_size()[0] * 0.015)
        self.pad_height = self.pad_height_half * 2

    def start(self):
        self.pad1_position = int(self.play_area.get_size()[1] / 2)
        self.pad2_position = int(self.play_area.get_size()[1] / 2)
        self.pad1_vel = 0
        self.pad2_vel = 0
        self.ball_velocity = [0, 0]
        self.pad1_pressed = False
        self.pad2_pressed = False
        self.ball_position = [self.play_area.get_size()[0] / 2,
                              self.play_area.get_size()[1] / 2]

    def reset(self):
        self.score = [0, 0]

    def game_over(self) -> None:
        return  # super().game_over()

    def _draw_ball(self):
        pygame.draw.rect(
            self.play_area,
            (200, 200, 200),
            [
                self.ball_position[0] - self.ball_radius,
                self.ball_position[1] - self.ball_radius,
                self.ball_radius * 2,
                self.ball_radius * 2
            ]
        )

    def _draw_pad1(self):
        self.pad1_position += self.pad1_vel
        if self.pad1_position - self.pad_height_half < 0:
            self.pad1_position = 0 + self.pad_height_half
        if self.pad1_position + self.pad_height_half > \
           self.canvas.get_size()[1]:
            self.pad1_position = \
                self.canvas.get_size()[1] - self.pad_height_half
        pygame.draw.rect(
            self.play_area,
            (160, 160, 160),
            [
                0,
                self.pad1_position - self.pad_height_half,
                self.pad_width,
                self.pad_height
            ]
        )
        self.pad1_vel *= 0.9

    def _draw_pad2(self):
        self.pad2_position += self.pad2_vel
        if self.pad2_position - self.pad_height_half < 0:
            self.pad2_position = 0 + self.pad_height_half
        if self.pad2_position + self.pad_height_half > \
           self.canvas.get_size()[1]:
            self.pad2_position = self.canvas.get_size()[1] - \
                self.pad_height_half
        pygame.draw.rect(
            self.play_area,
            (160, 160, 160),
            [
                self.play_area.get_size()[0] - self.pad_width,
                self.pad2_position - self.pad_height_half,
                self.pad_width,
                self.pad_height
            ]
        )
        self.pad2_vel *= 0.9

    def update(self):
        self._draw_court()
        self._draw_pad1()
        self._draw_pad2()
        self._draw_ball()
        self._ball_check()
        self.score_player1.echo(str(self.score[0]))
        self.score_player2.echo(str(self.score[1]))
        self.screen.blit(self.canvas, [0, 0])
        self.screen.blit(self.play_area, [1, 1])
        return False

    def control(self, keys, joystick):
        if joystick:
            if joystick['axis'][1] < 0:
                self.pad1_vel -= self.pad_acceleration * \
                    abs(joystick['axis'][1])
                self.pad1_pressed += self.delta_increment * \
                    abs(joystick['axis'][1])
            if joystick['axis'][1] > 0:
                self.pad1_vel += self.pad_acceleration * \
                    abs(joystick['axis'][1])
                self.pad1_pressed += self.delta_increment * \
                    abs(joystick['axis'][1])
            if joystick['axis'][4] < 0:
                self.pad2_vel -= self.pad_acceleration * \
                    abs(joystick['axis'][4])
                self.pad2_pressed += self.delta_increment * \
                    abs(joystick['axis'][4])
            if joystick['axis'][4] > 0:
                self.pad2_vel += self.pad_acceleration * \
                    abs(joystick['axis'][4])
                self.pad2_pressed += self.delta_increment * \
                    abs(joystick['axis'][4])
            if joystick['button'][10]:
                self.reset()
        if K_ESCAPE in keys:
            self.stop()
        if K_w in keys:
            self.pad1_vel -= self.pad_acceleration
            self.pad1_pressed += self.delta_increment
        if K_s in keys:
            self.pad1_vel += self.pad_acceleration
            self.pad1_pressed += self.delta_increment
        if K_UP in keys:
            self.pad2_vel -= self.pad_acceleration
            self.pad2_pressed += self.delta_increment
        if K_DOWN in keys:
            self.pad2_vel += self.pad_acceleration
            self.pad2_pressed += self.delta_increment

    def _ball_spawn(self):
        self.start()
        self.ball_velocity[0] = (random.randrange(100, 200) / 50.0 *
                                 self.court_side)
        self.ball_velocity[1] = 0
        # Make sure ball will never run without an angle
        while self.ball_velocity[1] == 0:
            self.ball_velocity[1] = (random.randrange(-50, 50) / 100.0) * -1
        if self.ball_velocity[1] >= -0.6 or self.ball_velocity[1] <= 0.6:
            self.ball_velocity[1] *= 2

    def _draw_court(self):
        # Clear court
        self.canvas.fill((0, 0, 0))  # Black
        self.play_area.fill((0, 0, 0))  # Black
        # Draw gutters
        pygame.draw.line(self.canvas, (100, 100, 100),
                         [0, 0],
                         [0,
                          self.canvas.get_size()[1] - 1])
        pygame.draw.line(self.canvas, (100, 100, 100),
                         [0, 0],
                         [self.canvas.get_size()[0] - 1, 0])
        pygame.draw.line(self.canvas, (100, 100, 100),
                         [self.canvas.get_size()[0] - 1, 0],
                         [self.canvas.get_size()[0] - 1,
                          self.canvas.get_size()[1]])
        pygame.draw.line(self.canvas, (100, 100, 100),
                         [0,
                          self.canvas.get_size()[1] - 1],
                         [self.canvas.get_size()[0] - 1,
                          self.canvas.get_size()[1] - 1])
        # Draw mid dashed line
        for i in range(0, self.play_area.get_size()[1], 5):
            pygame.draw.line(self.play_area, (128, 128, 128),
                             [self.play_area.get_size()[0] / 2,
                              4 + (i * 5)],
                             [self.play_area.get_size()[0] / 2,
                              16 + (i * 5)])

    def _ball_check(self):
        # update ball position
        self.ball_position[0] += self.ball_velocity[0]
        self.ball_position[1] += self.ball_velocity[1]
        # Bounces off of the top
        if self.ball_position[1] - self.ball_radius < 0:
            self.ball_velocity[1] *= -1
            self.sound.tone(300)
        # Bounces off of the bottom
        if self.ball_position[1] + self.ball_radius > \
           self.play_area.get_size()[1]:
            self.ball_velocity[1] *= -1
            self.sound.tone(300)
        # Bounces off of the left
        if self.ball_position[0] - self.ball_radius < self.pad_width:
            if ((self.ball_position[1] + self.ball_radius) >
                    (self.pad1_position - self.pad_height_half)) and \
               ((self.ball_position[1] - self.ball_radius) <
                    (self.pad1_position + self.pad_height_half)):
                self.ball_velocity[0] *= -1.1
                self.ball_velocity[1] *= 1.1
                self.sound.tone(900)
            else:
                self.court_side = -1
                self._ball_spawn()
                self.score[1] += 1
                self.sound.tone(200)
        # Bounces off of the right
        if self.ball_position[0] + self.ball_radius > \
           self.play_area.get_size()[0] - self.pad_width:
            if ((self.ball_position[1] + self.ball_radius) >
                    (self.pad2_position - self.pad_height_half)) and \
               ((self.ball_position[1] - self.ball_radius) <
                    (self.pad2_position + self.pad_height_half)):
                self.ball_velocity[0] *= -1.1
                self.ball_velocity[1] *= 1.1
                self.sound.tone(900)
            else:
                self.court_side = 1
                self._ball_spawn()
                self.score[0] += 1
                self.sound.tone(200)
