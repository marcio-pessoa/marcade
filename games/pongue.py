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
  - name: Gustavo Nuzzo Gass
    email: gustavonuzzogass@gmail.com
  - name: Nicolas Masaishi Oi Pessoa
    email: masaishi.pessoa@gmail.com
change-log: Check CHANGELOG.md file.
"""

import random
import pygame
from pygame.locals import *
from tools.font import Font
from tools.sound import Sound


class Pongue:  # pylint: disable=too-many-instance-attributes
    """
    description:
    """

    __version__ = 0.06

    def __init__(self, screen):
        self.screen = screen
        self.running = False
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
        self.screen_size = []
        self.court = 0
        self.play_area = 0
        self.score_player1 = 0
        self.score_player2 = 0

    def start(self):
        """
        description:
        """
        self.running = True
        self.size_set()
        self.pad_acceleration = 1
        self.delta_increment = 6
        self.court_side = 1
        self.reset()
        self.set()
        self.ball_spawn()
        self.score_player1 = Font(self.play_area)
        self.score_player1.set_size(5)
        self.score_player1.set_position([290, 20])
        self.score_player1.set_color((120, 120, 120))
        self.score_player2 = Font(self.play_area)
        self.score_player2.set_size(5)
        self.score_player2.set_position([480, 20])
        self.score_player2.set_color((120, 120, 120))

    def size_set(self):
        """
        description:
        """
        self.screen_size = [self.screen.get_size()[0],
                            self.screen.get_size()[1]]
        self.court = pygame.Surface(self.screen_size)
        self.play_area = pygame.Surface([self.court.get_size()[0] - 2,
                                         self.court.get_size()[1] - 2],
                                        pygame.SRCALPHA, 32)
        self.play_area.convert_alpha()
        # TODO: Set ball size based on both dimensions of window size
        self.ball_radius = int(self.play_area.get_size()[0] * 0.03 / 2)
        self.pad_height_half = int(self.play_area.get_size()[1] * 0.2 / 2)
        self.pad_width = int(self.play_area.get_size()[0] * 0.015)
        self.pad_height = self.pad_height_half * 2

    def size_reset(self):
        """
        description:
        """
        # Discover new size factor
        x_factor = self.screen.get_size()[0] / self.screen_size[0]
        y_factor = self.screen.get_size()[1] / self.screen_size[1]
        # Set objects new size
        self.ball_position[0] *= x_factor
        self.ball_position[1] *= y_factor
        # FIXME: Fix pads position
        self.pad1_position *= y_factor
        self.pad2_position *= y_factor
        # FIXME: Fix ball speed
        self.ball_velocity[0] *= x_factor
        self.ball_velocity[1] *= y_factor
        self.size_set()

    def set(self):
        """
        description:
        """
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
        """
        description:
        """
        self.score = [0, 0]

    def draw_ball(self):
        """
        description:
        """
        pygame.draw.rect(self.play_area, (200, 200, 200),
                         [self.ball_position[0] - self.ball_radius,
                          self.ball_position[1] - self.ball_radius,
                          self.ball_radius * 2, self.ball_radius * 2])

    def draw_pad1(self):
        """
        description:
        """
        self.pad1_position += self.pad1_vel
        if self.pad1_position - self.pad_height_half < 0:
            self.pad1_position = 0 + self.pad_height_half
        if self.pad1_position + self.pad_height_half > self.court.get_size()[1]:
            self.pad1_position = self.court.get_size()[1] - self.pad_height_half
        pygame.draw.rect(self.play_area, (160, 160, 160),
                         [0,
                          self.pad1_position - self.pad_height_half,
                          self.pad_width,
                          self.pad_height])
        self.pad1_vel *= 0.9

    def draw_pad2(self):
        """
        description:
        """
        self.pad2_position += self.pad2_vel
        if self.pad2_position - self.pad_height_half < 0:
            self.pad2_position = 0 + self.pad_height_half
        if self.pad2_position + self.pad_height_half > self.court.get_size()[1]:
            self.pad2_position = self.court.get_size()[1] - self.pad_height_half
        pygame.draw.rect(self.play_area, (160, 160, 160),
                         [self.play_area.get_size()[0] - self.pad_width,
                          self.pad2_position - self.pad_height_half,
                          self.pad_width,
                          self.pad_height])
        self.pad2_vel *= 0.9

    def run(self):
        """
        description:
        """
        self.draw_court()
        self.draw_pad1()
        self.draw_pad2()
        self.draw_ball()
        self.ball_check()
        self.score_player1.echo(str(self.score[0]))
        self.score_player2.echo(str(self.score[1]))
        self.screen.blit(self.court, [0, 0])
        self.screen.blit(self.play_area, [1, 1])
        return False

    def stop(self):
        """
        description:
        """
        pygame.event.clear()
        self.running = False

    def control(self, keys, joystick):
        """
        description:
        """
        if joystick:
            if joystick['axis'][1] < 0:
                self.pad1_vel -= self.pad_acceleration * abs(joystick['axis'][1])
                self.pad1_pressed += self.delta_increment * abs(joystick['axis'][1])
            if joystick['axis'][1] > 0:
                self.pad1_vel += self.pad_acceleration * abs(joystick['axis'][1])
                self.pad1_pressed += self.delta_increment * abs(joystick['axis'][1])
            if joystick['axis'][4] < 0:
                self.pad2_vel -= self.pad_acceleration * abs(joystick['axis'][4])
                self.pad2_pressed += self.delta_increment * abs(joystick['axis'][4])
            if joystick['axis'][4] > 0:
                self.pad2_vel += self.pad_acceleration * abs(joystick['axis'][4])
                self.pad2_pressed += self.delta_increment * abs(joystick['axis'][4])
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

    def ball_spawn(self):
        """
        initialize ball_pos and ball_vel for new bal in middle of table
        if direction is RIGHT, the ball's velocity is upper right, else
        upper left
        """
        self.set()
        self.ball_velocity[0] = (random.randrange(100, 200) / 50.0 *
                                 self.court_side)
        self.ball_velocity[1] = 0
        # Make sure ball will never run without an angle
        while self.ball_velocity[1] == 0:
            self.ball_velocity[1] = (random.randrange(-50, 50) / 100.0) * -1
        if self.ball_velocity[1] >= -0.6 or self.ball_velocity[1] <= 0.6:
            self.ball_velocity[1] *= 2

    def draw_court(self):
        """
        description:
        """
        # Clear court
        self.court.fill([0, 0, 0])  # Black
        self.play_area.fill([0, 0, 0])  # Black
        # Draw gutters
        pygame.draw.line(self.court, (100, 100, 100),
                         [0, 0],
                         [0,
                          self.court.get_size()[1] - 1])
        pygame.draw.line(self.court, (100, 100, 100),
                         [0, 0],
                         [self.court.get_size()[0] - 1, 0])
        pygame.draw.line(self.court, (100, 100, 100),
                         [self.court.get_size()[0] - 1, 0],
                         [self.court.get_size()[0] - 1,
                          self.court.get_size()[1]])
        pygame.draw.line(self.court, (100, 100, 100),
                         [0,
                          self.court.get_size()[1] - 1],
                         [self.court.get_size()[0] - 1,
                          self.court.get_size()[1] - 1])
        # Draw mid dashed line
        for i in range(0, self.play_area.get_size()[1], 5):
            pygame.draw.line(self.play_area, (128, 128, 128),
                             [self.play_area.get_size()[0] / 2,
                              4 + (i * 5)],
                             [self.play_area.get_size()[0] / 2,
                              16 + (i * 5)])

    def ball_check(self):
        """
        description:
        """
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
                self.ball_spawn()
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
                self.ball_spawn()
                self.score[0] += 1
                self.sound.tone(200)
