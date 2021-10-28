"""
---
name: rocks.py
description: Rocks game package file
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  designers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
  - name: Nicolas Masaishi Oi Pessoa
    email: masaishi.pessoa@gmail.com
  - name: Gustavo Nuzzo Gass
    email: gustavonuzzogass@gmail.com
  beta-testers:
  - name: Gustavo Nuzzo Gass
    email: gustavonuzzogass@gmail.com
  - name: Nicolas Masaishi Oi Pessoa
    email: masaishi.pessoa@gmail.com
change-log: Check CHANGELOG.md file.
"""

import math
import random
import pygame
from pygame.locals import *
from tools.font import Font
from tools.sound import Sound


class Rocks:
    """
    description:
    """

    __version__ = '0.05'

    def __init__(self, screen):
        self.screen = screen
        self.running = False
        self.sound = Sound()

    def start(self):
        """
        description:
        """
        self.running = True
        self.size_set()
        self.pad_acceleration = 1
        self.court_side = 1
        self.set()
        self.ship.start()
        self.scoreboard = Font(self.space)
        self.scoreboard.set_size(3)
        self.scoreboard.set_position([10, 10])
        self.scoreboard.set_color((100, 100, 100))
        self.livesboard = Font(self.space)
        self.livesboard.set_size(3)
        self.livesboard.set_position([300, 10])
        self.livesboard.set_color((100, 100, 100))

    def size_set(self):
        """
        description:
        """
        self.screen_size = [self.screen.get_size()[0],
                            self.screen.get_size()[1]]
        self.space = pygame.Surface(self.screen_size,
                                    HWSURFACE | SRCALPHA, 32)
        self.space.convert_alpha()

    def set(self):
        """
        description:
        """
        self.ship = Ship(self.space)
        self.reset()

    def size_reset(self):
        """
        description:
        """
        # Discover new size factor
        x_factor = self.screen.get_size()[0] / self.screen_size[0]
        y_factor = self.screen.get_size()[1] / self.screen_size[1]
        self.size_set()
        self.ship.screen_reset()

    def reset(self):
        """
        description:
        """
        self.lives = 3
        self.score = 0
        self.rock_group = set()
        self.burst = set()
        self.ship.reset()

    def run(self):
        """
        description:
        """
        # Draw Space
        self.space.fill([0, 0, 0])  # Black
        # Draw objects (ship, rocks, missiles, etc...)
        self.ship.update()
        self.burst_update()
        self.rock_update()
        self.check_collision()
        self.update_scoreboard()
        if not self.lives:
            self.reset()
        # Join everything
        self.screen.blit(self.space, [0, 0])
        return False

    def update_scoreboard(self):
        """
        description:
        """
        self.scoreboard.echo(str(self.score))
        self.livesboard.echo(str(self.lives))
        if self.score % 100 == 1 and self.score != 1:
            self.score += 10
            self.lives += 1

    def check_collision(self):
        """
        description:
        """
        for i in self.rock_group:
            # Ship against rocks
            if i.get_rect().colliderect(self.ship.get_rect()):
                self.rock_group.remove(i)
                self.lives -= 1
                return
            # Missile against rocks
            for j in self.burst:
                if j.get_rect().colliderect(i.get_rect()):
                    self.rock_group.remove(i)
                    self.burst.remove(j)
                    self.score += 1
                    return
            # Rock against rocks
            for j in self.rock_group:
                if j == i:
                    continue
                if j.get_rect().colliderect(i.get_rect()):
                    i.upgrade(j.get_size())
                    self.rock_group.remove(j)
                    return
        # Missile against ship
        for i in self.burst:
            if i.get_rect().colliderect(self.ship.get_rect()):
                self.burst.remove(i)
                return

    def rock_update(self):
        """
        description:
        """
        # Need more?
        while len(self.rock_group) < 8:
            rock = Sprite(self.space)
            if not rock.get_rect().colliderect(self.ship.get_double_rect()):
                self.rock_group.add(rock)
        # Update position
        for i in self.rock_group:
            i.update()

    def burst_update(self):
        """
        description:
        """
        # Update position
        for i in self.burst:
            i.update()
        # Check shoot age
        for i in self.burst:
            if i.age() >= 3000:
                self.burst.remove(i)
                break

    def stop(self):
        """
        description:
        """
        pygame.event.clear()
        self.running = False

    def shoot(self):
        """
        description:
        """
        # Limit burst size
        if len(self.burst) >= 10:
            return
        # Shoot!
        shoot = Missile(self.space,
                        self.ship.get_position(), self.ship.get_radius(),
                        self.ship.get_speed(), self.ship.get_angle())
        self.burst.add(shoot)
        self.sound.tone(800)

    def control(self, keys, joystick):
        """
        description:
        """
        if joystick:
            if joystick['hat'][0]['x'] < 0 or \
               joystick['axis'][0] < 0:
                self.ship.increment_angle_vel()
            if joystick['hat'][0]['x'] > 0 or \
               joystick['axis'][0] > 0:
                self.ship.decrement_angle_vel()
            if joystick['hat'][0]['y'] > 0 or \
               joystick['axis'][1] < 0:
                self.ship.thrust_on()
                return
            if joystick['button'][10]:
                self.reset()
            if joystick['button'][0]:
                self.shoot()
        if K_ESCAPE in keys:  # pylint: disable=undefined-variable
            self.stop()
        if K_UP in keys:
            self.ship.thrust_on()
        if K_UP not in keys:
            self.ship.thrust_off()
        if K_RIGHT in keys:
            self.ship.decrement_angle_vel()
        if K_LEFT in keys:
            self.ship.increment_angle_vel()
        if K_SPACE in keys or \
           K_a in keys:
            self.shoot()


class Ship:
    """
    description:
    """

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0],
                            self.screen.get_size()[1]]
        self.reset()

    def reset(self):
        """
        description:
        """
        self.position = [self.screen_size[0] / 2, self.screen_size[1] / 2]
        self.speed = [0, 0]
        self.angle = math.pi / -2
        self.thrust = False
        self.angle_vel = 0

    def start(self):
        """
        description:
        """
        self.ship_size = [31, 31]
        position = [0, 0]
        ship = pygame.Surface(self.ship_size, SRCALPHA)
        # Draw ship
        pygame.draw.polygon(ship, (200, 200, 200),
                            [(0, 30), (15, 0), (30, 30), (15, 23)], 0)
        self.ship = pygame.Surface([48, 48], SRCALPHA)
        ship = pygame.transform.rotate(ship, 90)
        position[0] = self.ship.get_rect().center[0] - ship.get_rect().center[0]
        position[1] = self.ship.get_rect().center[1] - ship.get_rect().center[1]
        self.ship.blit(ship, position)
        self.__rect = ship.get_rect()
        self.radius = self.ship.get_rect().center[1]
        self.update()

    def update(self):
        """
        description:
        """
        # Angle
        acc = []
        self.angle += self.angle_vel
        # Position
        self.position[0] = ((self.position[0] + self.speed[0]) %
                            self.screen_size[0])
        self.position[1] = ((self.position[1] + self.speed[1]) %
                            self.screen_size[1])
        position = (self.position[0] - self.radius,
                    self.position[1] - self.radius)
        # Speed
        if self.thrust:
            acc = [-math.cos(self.angle), math.sin(self.angle)]
            self.speed[0] += acc[0] * .2
            self.speed[1] += acc[1] * .2
        # Slow down
        self.speed[0] *= .99
        self.speed[1] *= .99
        # Draw
        orig_rect = self.ship.get_rect()
        rot_image = pygame.transform.rotozoom(self.ship,
                                              math.degrees(self.angle), 1)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        ship = rot_image.subsurface(rot_rect).copy()
        self.rect = self.__rect.move(position)
        self.screen.blit(ship, position)
        ship_double_size = [self.ship_size[0] * 4, self.ship_size[1] * 4]
        __ship_double = pygame.Surface(ship_double_size, SRCALPHA)
        self.double_rect = __ship_double.get_rect()

    def thrust_on(self):
        """
        description:
        """
        self.thrust = True

    def thrust_off(self):
        """
        description:
        """
        # ship_thrust_sound.pause()
        self.thrust = False

    def increment_angle_vel(self):
        """
        description:
        """
        self.angle_vel += math.radians(math.pi / 50)

    def decrement_angle_vel(self):
        """
        description:
        """
        self.angle_vel -= math.radians(math.pi / 50)

    def get_rect(self):
        """
        description:
        """
        return self.rect

    def get_double_rect(self):
        """
        description:
        """
        return self.double_rect

    def get_radius(self):
        """
        description:
        """
        return self.radius

    def get_position(self):
        """
        description:
        """
        return self.position

    def get_speed(self):
        """
        description:
        """
        return self.speed

    def get_angle(self):
        """
        description:
        """
        return self.angle


class Missile:
    """
    description:
    """

    def __init__(self, screen,
                 ship_position, ship_radius, ship_speed, ship_angle,):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0],
                            self.screen.get_size()[1]]
        self.angle = ship_angle
        forward = [-math.cos(self.angle), math.sin(self.angle)]
        self.position = [ship_position[0] + ship_radius * forward[0],
                         ship_position[1] + ship_radius * forward[1]]
        self.speed = [ship_speed[0] + 5 * forward[0],
                      ship_speed[1] + 5 * forward[1]]
        self.radius = 3
        size = [self.radius * 2, self.radius * 2]
        position = [self.radius, self.radius]
        self.missile = pygame.Surface(size, SRCALPHA)
        pygame.draw.circle(self.missile, (210, 210, 210), position, self.radius)
        self.time_born = pygame.time.get_ticks()
        self.update()

    def update(self):
        """
        description:
        """
        self.position[0] = ((self.position[0] + self.speed[0]) %
                            self.screen_size[0])
        self.position[1] = ((self.position[1] + self.speed[1]) %
                            self.screen_size[1])
        position = (self.position[0] - self.radius,
                    self.position[1] - self.radius)
        self.rect = self.missile.get_rect().move(position)
        self.screen.blit(self.missile, position)

    def age(self):
        """
        description:
        """
        return pygame.time.get_ticks() - self.time_born

    def get_radius(self):
        """
        description:
        """
        return self.radius

    def get_rect(self):
        """
        description:
        """
        return self.rect


class Sprite:
    """
    description:
    """

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0],
                            self.screen.get_size()[1]]
        self.position = [random.uniform(0.0, 1.0) * self.screen_size[0],
                         random.uniform(0.0, 1.0) * self.screen_size[1]]
        self.speed = [random.uniform(-0.5, 0.5),
                      random.uniform(-0.5, 0.5)]
        self.angle = 0
        self.angle_vel = math.radians(math.pi / (random.uniform(-1, 1) * 10.1))
        self.size = [31, 31]
        size = self.size
        position = [0, 0]
        ship = pygame.Surface(self.size, SRCALPHA)
        color_tone = random.randrange(50, 100)
        pygame.draw.polygon(ship,
                            [color_tone, color_tone, color_tone],
                            [(random.uniform(0, size[1] / 4),
                              random.uniform(0, size[1] / 3)),
                             (random.uniform(size[0] / 4, size[1] / 1.5),
                              random.uniform(0, size[1] / 2)),
                             (random.uniform(size[0] / 1.5, size[1]),
                              random.uniform(0, size[1] / 2)),
                             (random.uniform(size[0] / 1.1, size[1]),
                              random.uniform(size[0] / 1.5, size[1])),
                             (random.uniform(size[0] / 3, size[1] / 1.5),
                              random.uniform(size[0] / 1.5, size[1])),
                             (random.uniform(0, size[1] / 4),
                              random.uniform(size[0] / 1.5, size[1])),
                             ], 0)
        self.ship = pygame.Surface([48, 48], SRCALPHA)
        position[0] = self.ship.get_rect().center[0] - ship.get_rect().center[0]
        position[1] = self.ship.get_rect().center[1] - ship.get_rect().center[1]
        self.ship.blit(ship, position)
        self.__rect = ship.get_rect()
        __spawn_far = pygame.Surface([80, 80], SRCALPHA).get_rect()
        self.radius = self.ship.get_rect().center[1]
        self.update()

    def upgrade(self, size):
        """
        description:
        """
        self.size[0] += size[0]
        self.size[1] += size[1]
        size = self.size
        self.ship = pygame.Surface(self.size, SRCALPHA)
        color_tone = random.randrange(50, 100)
        pygame.draw.polygon(
            self.ship,
            [color_tone, color_tone, color_tone],
            [(random.uniform(0, size[1] / 4),
              random.uniform(0, size[1] / 3)),
             (random.uniform(size[0] / 4, size[1] / 1.5),
              random.uniform(0, size[1] / 2)),
             (random.uniform(size[0] / 1.5, size[1]),
              random.uniform(0, size[1] / 2)),
             (random.uniform(size[0] / 1.1, size[1]),
              random.uniform(size[0] / 1.5, size[1])),
             (random.uniform(size[0] / 3, size[1] / 1.5),
              random.uniform(size[0] / 1.5, size[1])),
             (random.uniform(0, size[1] / 4),
              random.uniform(size[0] / 1.5, size[1])),
             ], 0)
        self.radius = self.ship.get_rect().center[1]
        self.__rect = self.ship.get_rect()
        self.update()

    def update(self):
        """
        description:
        """
        # Angle
        self.angle += self.angle_vel
        # Position
        self.position[0] = ((self.position[0] + self.speed[0]) %
                            self.screen_size[0])
        self.position[1] = ((self.position[1] + self.speed[1]) %
                            self.screen_size[1])
        position = (self.position[0] - self.radius,
                    self.position[1] - self.radius)
        # Draw
        orig_rect = self.ship.get_rect()
        rot_image = pygame.transform.rotozoom(self.ship,
                                              math.degrees(self.angle), 1)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        ship = rot_image.subsurface(rot_rect).copy()
        self.radius = ship.get_rect().center[0]
        self.rect = self.__rect.move(position)
        self.screen.blit(ship, position)

    def get_size(self):
        """
        description:
        """
        return self.size

    def get_rect(self):
        """
        description:
        """
        return self.rect
