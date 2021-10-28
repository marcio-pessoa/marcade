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
  - name: Gustavo Nuzzo Gass
    email: gustavonuzzogass@gmail.com
change-log: Check CHANGELOG.md file.
"""

import random
import pygame
from pygame.locals import *  # pylint: disable=wildcard-import
from tools.font import Font
from tools.sound import Sound
from tools.timer.timer import Timer


class Invasion:  # pylint: disable=too-many-instance-attributes
    """
    description:
    """

    __version__ = 0.5

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0], self.screen.get_size()[1]]
        self.space = pygame.Surface(self.screen_size,
                                    HWSURFACE | SRCALPHA, 32)  # pylint: disable=undefined-variable
        self.space.convert_alpha()
        self.running = True
        self.ship_burst = set()
        self.alien_burst = set()
        self.walls = set()
        self.aliens = set()
        self.explosions = set()
        self.ship = Ship(self.space)
        self.shoot_timer = Timer(50)
        self.march_timer = Timer(1)
        self.scoreboard = Font(self.space)
        self.scoreboard.set_size(3)
        self.scoreboard.set_position([10, 5])
        self.livesboard = Font(self.space)
        self.livesboard.set_size(3)
        self.livesboard.set_position([330, 5])
        self.levelboard = Font(self.space)
        self.levelboard.set_size(3)
        self.levelboard.set_position([580, 5])
        self.gameovermessage = Font(self.space)
        self.gameovermessage.set_size(9)
        self.gameovermessage.set_position([180, 60])
        self.gameovermessage.set_color((230, 230, 230))
        self.sound = Sound()
        self.reset()

    def set(self):
        """
        description:
        """
        self.ship_burst = set()
        self.alien_burst = set()
        self.walls = set()
        self.aliens = set()
        self.explosions = set()
        self.alien_burst_seed = 2000
        self.march_period = self.start_march_period
        self.march_timer.set(self.march_period)
        self.way = True
        self.drop = False
        self.ship.reset()
        self._walls_deploy()
        self._aliens_deploy()

    def reset(self):
        """
        description:
        """
        self.level = 0
        self.lives = 2
        self.score = 0
        self.start_march_period = 600
        self.set()
        self._level_up()

    def run(self):
        """
        description:
        """
        self.space.fill([0, 0, 0])  # Black
        self._score_update()
        self._burst_update()
        self._walls_update()
        self.ship.update()
        self._aliens_update()
        self._explosions_update()
        self._collision_check()
        self._aliens_check()
        self._lives_check()
        self.screen.blit(self.space, [0, 0])
        return False

    def control(self, keys, joystick):
        """
        description:
        """
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
        if K_ESCAPE in keys:  # pylint: disable=undefined-variable
            self._stop()
        if K_RIGHT in keys:  # pylint: disable=undefined-variable
            self.ship.move_right()
        if K_LEFT in keys:  # pylint: disable=undefined-variable
            self.ship.move_left()
        if K_SPACE in keys or K_a in keys:  # pylint: disable=undefined-variable
            self._ship_shoot()
        if K_RETURN in keys:  # pylint: disable=undefined-variable
            self.reset()

    def _lives_check(self):
        if self.lives == 0:
            self._game_over()

    def _collision_check(self):  # pylint: disable=too-many-branches
        # Ship Missle against Alien
        for i in self.aliens:
            for j in self.ship_burst:
                if i.rect.colliderect(j.rect):
                    position = i.get_position()
                    explosion = Explosion(self.space, position)
                    self.explosions.add(explosion)
                    self.score += i.points
                    self.aliens.remove(i)
                    self.ship_burst.remove(j)
                    self.sound.tone(400)
                    return
        # Ship Missle against Wall
        for i in self.walls:
            for j in self.ship_burst:
                if i.rect.colliderect(j.rect):
                    self.score += i.points
                    if i.add_damage() <= 0:
                        self.walls.remove(i)
                    self.ship_burst.remove(j)
                    self.sound.tone(200)
                    return
        # Alien Missle against Wall
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
                    position = i.get_position()
                    explosion = Explosion(self.space, position)
                    self.explosions.add(explosion)
                    position = j.get_position()
                    explosion = Explosion(self.space, position)
                    self.explosions.add(explosion)
                    self.aliens.remove(i)
                    self.walls.remove(j)
                    self.sound.tone(200)
                    return
        # Ship against Alien
        for i in self.aliens:
            if i.rect.colliderect(self.ship.rect):
                position = i.get_position()
                explosion = Explosion(self.space, position)
                self.explosions.add(explosion)
                position = self.ship.get_position()
                explosion = Explosion(self.space, position)
                self.explosions.add(explosion)
                self.aliens.remove(i)
                self.lives -= 1
                self.sound.tone(200)
                return
        # Alien Missle againt Ship
        for i in self.alien_burst:
            if i.rect.colliderect(self.ship.rect):
                position = self.ship.get_position()
                explosion = Explosion(self.space, position)
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
            if i.is_out():
                self.ship_burst.remove(i)
                break

    def _aliens_deploy(self):
        formation = (7, 6)
        for cartesian_y in range(formation[1]):
            for cartesian_x in range(formation[0]):
                monster = Monster(self.space, cartesian_y,
                                  [(self.screen_size[0] /
                                    formation[0]) * cartesian_x +
                                   (self.screen_size[0] /
                                    formation[0]) / 3,
                                   ((self.screen_size[1] /
                                     (formation[1] + 3) * cartesian_y)) + 30])
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
                if not self.space.get_rect().contains(i.rect):
                    self.way = not self.way
                    if self.way:
                        self.drop = True
                        self.march_period /= 1.15
                        self.march_timer.set(self.march_period)
                    break
            # Aliens fall down
            for i in self.aliens:
                i.march(self.way, self.drop)
            self.drop = False
        # Aliens landing
        for i in self.aliens:
            if i.get_position()[1] + i.get_size()[1] >= self.screen_size[1]:
                self._game_over()
                break
        # Fire
        for i in self.aliens:
            i.update()
            if random.randrange(self.alien_burst_seed) == 1:
                shoot = Missile(self.space,
                                i.get_position(), i.get_radius(), 4, -1)
                self.alien_burst.add(shoot)
                break

    def _game_over(self):
        self.ship.stop()
        for i in self.aliens:
            i.stop()
        for i in self.ship_burst:
            i.stop()
        for i in self.alien_burst:
            i.stop()
        self.gameovermessage.echo("GAME OVER")

    def _aliens_check(self):
        if len(self.aliens) == 0:
            self._level_up()

    def _level_up(self):
        self.level += 1
        self.lives += 1
        self.alien_burst_seed -= self.level * 100
        self.start_march_period -= self.start_march_period * self.level / 20
        self.set()

    def _walls_deploy(self):
        quantity = 4
        for i in range(quantity):
            position = (self.screen.get_size()[0] / quantity * i +
                        (self.screen.get_size()[0] / quantity / 2 - 24), 400)
            barrier = Barrier(self.space, position)
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

    def _stop(self):
        pygame.event.clear()
        self.running = False

    def _ship_shoot(self):
        # Limit shoot frequency
        if not self.shoot_timer.check():
            return
        # Limit burst size
        if len(self.ship_burst) >= 1:
            return
        # Shoot!
        shoot = Missile(self.space,
                        self.ship.get_position(), self.ship.get_radius(), 5)
        self.ship_burst.add(shoot)
        self.sound.tone(1200)


class Ship:  # pylint: disable=too-many-instance-attributes
    """
    description:
    """

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0], self.screen.get_size()[1]]
        self.size = [48, 32]
        self.color = (180, 180, 240)
        self.enable = True
        sprite = \
            (
                "            ",
                "     ##     ",
                "    ####    ",
                "   ######   ",
                " ########## ",
                "  ########  ",
                " ########## ",
                "############",
            )
        self.move_increment = 5
        self.reset()
        self.shape = pygame.Surface(self.size, SRCALPHA)  # pylint: disable=undefined-variable
        draw(self.shape, sprite, self.color, 4)
        self.radius = self.shape.get_rect().center[0]

    def reset(self):
        """
        description:
        """
        self.position = [self.screen_size[0] / 2,
                         self.screen_size[1] - self.size[1]]
        self.start()

    def update(self):
        """
        description:
        """
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[0] + self.size[0] > self.screen.get_size()[0]:
            self.position[0] = self.screen.get_size()[0] - self.size[0]
        self.rect = self.shape.get_rect().move(self.position)
        self.screen.blit(self.shape, self.position)

    def move_right(self):
        """
        description:
        """
        if not self.enable:
            return
        self.position[0] += self.move_increment

    def move_left(self):
        """
        description:
        """
        if not self.enable:
            return
        self.position[0] -= self.move_increment

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

    def start(self):
        """
        description:
        """
        self.enable = True

    def stop(self):
        """
        description:
        """
        self.enable = False


class Missile:   # pylint: disable=too-many-arguments,too-many-instance-attributes
    """
    description:
    """

    def __init__(self, screen, ship_position, offset, speed, direction=1):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0], self.screen.get_size()[1]]
        self.out = False
        self.size = [8, 16]
        self.speed = speed * direction
        self.color = (250, 250, 250)
        sprite = \
            (
                "##",
                "##",
                "##",
                "##",
            )
        self.shape = pygame.Surface(self.size, SRCALPHA)  # pylint: disable=undefined-variable
        draw(self.shape, sprite, self.color, 4)
        if direction == 1:
            self.position = [ship_position[0] + offset - self.size[0] / 2,
                             ship_position[1] - self.size[1]]
        elif direction == -1:
            self.position = [ship_position[0] + offset - self.size[0] / 2,
                             ship_position[1] + self.size[1] + 20]
        self.enable = True
        self.update()

    def update(self):
        """
        description:
        """
        if self.enable:
            self.position[1] = self.position[1] - self.speed
        if self.position[1] < 0:
            self.out = True
        self.rect = self.shape.get_rect().move(self.position)
        self.screen.blit(self.shape, self.position)

    def is_out(self):
        """
        description:
        """
        return self.out

    def stop(self):
        """
        description:
        """
        self.enable = False


class Monster:  # pylint: disable=too-many-instance-attributes
    """
    description:
    """

    def __init__(self, screen, aspect, position):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0], self.screen.get_size()[1]]
        self.aspect = aspect % 6
        self.__color = \
            [
                (150, 200, 100),
                (200, 200, 100),
                (100, 200, 200),
                (200, 100, 200),
                (100, 100, 200),
                (200, 100, 100)
            ]
        self.position = position
        self.alien = self._sprite(self.aspect)
        self.size = [48, 32]
        self._color = self.__color[self.aspect]
        self.shape = pygame.Surface(self.size, SRCALPHA)  # pylint: disable=undefined-variable
        self.caray = 0
        self.radius = self.shape.get_rect().center[0]
        draw(self.shape, self.alien[0], self._color, 4)
        self.points = 10 - aspect
        self.enable = True

    def _sprite(self, monster):
        aliens = \
            (
                (
                    (
                        "    ####    ",
                        " ########## ",
                        "############",
                        "###  ##  ###",
                        "############",
                        "   ##  ##   ",
                        "  ## ## ##  ",
                        "##        ##",
                    ), (
                        "    ####    ",
                        " ########## ",
                        "############",
                        "###  ##  ###",
                        "############",
                        "  ###  ###  ",
                        " ##  ##  ## ",
                        "  ##    ##  ",
                    )
                ),
                (
                    (
                        "  #      #  ",
                        "   #    #   ",
                        "  ########  ",
                        " ## #### ## ",
                        "############",
                        "# ######## #",
                        "# #      # #",
                        "   ##  ##   ",
                    ), (
                        "  #      #  ",
                        "#  #    #  #",
                        "# ######## #",
                        "### #### ###",
                        "############",
                        " ########## ",
                        "  #      #  ",
                        " #        # ",
                    )
                ),
                (
                    (
                        "    ####    ",
                        "#####  #####",
                        "# ######## #",
                        "#  ######  #",
                        "#  ######   ",
                        "#   ####    ",
                        "    #  #    ",
                        "    #  ##   ",
                    ), (
                        "    ####    ",
                        "#####  #####",
                        "# ######## #",
                        "#  ######  #",
                        "   ######  #",
                        "    ####   #",
                        "    #  #    ",
                        "   ##  #    ",
                    )
                ),
                (
                    (
                        "   ##  ##   ",
                        "     ##     ",
                        "#### ## ####",
                        " ########## ",
                        "  ########  ",
                        "   ######   ",
                        "    #  #    ",
                        "    #  #    ",
                    ), (
                        "   ##  ##   ",
                        "     ##     ",
                        "  ## ## ##  ",
                        "  ########  ",
                        "   ######   ",
                        "    ####    ",
                        "    #  #    ",
                        "    #  #    ",
                    )
                ),
                (
                    (
                        "    #  #    ",
                        "   ######  #",
                        "  ## ## ## #",
                        "#### ## ####",
                        "# ########  ",
                        "# ########  ",
                        "   #    #   ",
                        "  ##    #   ",
                    ), (
                        "    #  #    ",
                        "#  ######   ",
                        "# ## ## ##  ",
                        "#### ## ####",
                        "  ######## #",
                        "  ######## #",
                        "   #    #   ",
                        "   #    ##  ",
                    )
                ),
                (
                    (
                        "  #      #  ",
                        "   #    #   ",
                        "   ######   ",
                        " # ##  ## # ",
                        " ########## ",
                        " #   ##   # ",
                        " #       # #",
                        "# #         ",
                    ), (
                        "  #      #  ",
                        "   #    #   ",
                        "   ######   ",
                        " # ##  ## # ",
                        " ########## ",
                        " #   ##   # ",
                        "# #       # ",
                        "         # #",
                    )
                ),
                (
                    (
                        "  #      #  ",
                        "   #    #   ",
                        "  ########  ",
                        " ## #### ## ",
                        "### #### ###",
                        "# ######## #",
                        "# #      # #",
                        "  ##    ##  ",
                    ), (
                        "  #      #  ",
                        "#  #    #  #",
                        "# ######## #",
                        "### #### ###",
                        "### #### ###",
                        " ########## ",
                        " # #    # # ",
                        "##        ##",
                    )
                ),
                (
                    (
                        "    ####    ",
                        " ########## ",
                        "############",
                        "#   ####   #",
                        "############",
                        "   #    #   ",
                        "  # #### #  ",
                        " #        # ",
                    ), (
                        "    ####    ",
                        " ########## ",
                        "############",
                        "#   ####   #",
                        "############",
                        "   # ## #   ",
                        "  #      #  ",
                        "   #    #   ",
                    )
                )
            )
        return aliens[monster]

    def update(self):
        """
        description:
        """
        self.rect = self.shape.get_rect().move(self.position)
        self.screen.blit(self.shape, self.position)

    def march(self, way, drop):
        """
        description:
        """
        if not self.enable:
            return
        if way:
            increment = 1
        else:
            increment = -1
        self.position[0] += increment * 4
        if drop:
            self.position[1] += increment * 16
        draw(self.shape, self.alien[self.caray], self._color, 4)
        self.caray = (self.caray + 1) % 2

    def get_position(self):
        """
        description:
        """
        return self.position

    def get_radius(self):
        """
        description:
        """
        return self.radius

    def get_size(self):
        """
        description:
        """
        return self.size

    def stop(self):
        """
        description:
        """
        self.enable = False


class Barrier:  # pylint: disable=too-many-instance-attributes
    """
    description:
    """

    def __init__(self, screen, position):
        self.screen = screen
        self.screen_size = [self.screen.get_size()[0], self.screen.get_size()[1]]
        self.position = position
        self.size = [48, 32]
        self.color = (139, 105, 20)
        self.sprites = \
            (
                (
                    "            ",
                    "            ",
                    "            ",
                    "            ",
                    "            ",
                    "     ####   ",
                    "  ######### ",
                    "###      ###",
                ),
                (
                    "            ",
                    "            ",
                    "            ",
                    "            ",
                    "      ##    ",
                    "    #####   ",
                    " ########## ",
                    "###      ###",
                ),
                (
                    "            ",
                    "            ",
                    "     ##     ",
                    "   ######   ",
                    "    ######  ",
                    "  ########  ",
                    "############",
                    "###      ###",
                ),
                (
                    "            ",
                    "            ",
                    "     ##     ",
                    "   ######   ",
                    "   #######  ",
                    " ########## ",
                    "############",
                    "###      ###",
                ),
                (
                    "            ",
                    "    ###     ",
                    "   #####    ",
                    "  ########  ",
                    "  ########  ",
                    "########### ",
                    "############",
                    "###      ###",
                ),
                (
                    "    ####    ",
                    "  ########  ",
                    " ########## ",
                    " ########## ",
                    " ########## ",
                    "############",
                    "############",
                    "###      ###",
                )
            )
        self.status = len(self.sprites) - 1
        self.shape = pygame.Surface(self.size, SRCALPHA)  # pylint: disable=undefined-variable
        draw(self.shape, self.sprites[self.status], self.color, 4)
        self.points = 1

    def update(self):
        """
        description:
        """
        self.rect = self.shape.get_rect().move(self.position)
        self.screen.blit(self.shape, self.position)

    def add_damage(self):
        """
        description:
        """
        self.status -= 1
        draw(self.shape, self.sprites[self.status], self.color, 4)
        return self.status

    def get_position(self):
        """
        description:
        """
        return self.position


class Explosion:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """
    description:
    """

    def __init__(self, screen, position):
        self.screen = screen
        self.position = position
        self.update_timer = Timer(50)
        self.done = False
        self.sprites = \
            (
                (
                    "     ##     ",
                    "   ######   ",
                    " ########## ",
                    "############",
                    "############",
                    " ########## ",
                    "   ######   ",
                    "     ##     ",
                ),
                (
                    "            ",
                    "     ##     ",
                    "   ######   ",
                    " ########## ",
                    " ########## ",
                    "   ######   ",
                    "     ##     ",
                    "            ",
                ),
                (
                    "            ",
                    "            ",
                    "     ##     ",
                    "   ######   ",
                    "   ######   ",
                    "     ##     ",
                    "            ",
                    "            ",
                ),
                (
                    "            ",
                    "            ",
                    "            ",
                    "     ##     ",
                    "     ##     ",
                    "            ",
                    "            ",
                    "            ",
                ),
                (
                    "            ",
                    "            ",
                    "    #  #    ",
                    "     ##     ",
                    "     ##     ",
                    "    #  #    ",
                    "            ",
                    "            ",
                ),
                (
                    "            ",
                    "   #    #   ",
                    "    #  #    ",
                    "     ##     ",
                    "     ##     ",
                    "    #  #    ",
                    "   #    #   ",
                    "            ",
                ),
                (
                    "  #      #  ",
                    "   #    #   ",
                    "    #  #    ",
                    "     ##     ",
                    "     ##     ",
                    "    #  #    ",
                    "   #    #   ",
                    "  #      #  ",
                ),
                (
                    "  #      #  ",
                    "   #    #   ",
                    "    #  #  # ",
                    "            ",
                    " #          ",
                    "    #  #    ",
                    "   #    #   ",
                    "  #      #  ",
                ),
                (
                    "  #      #  ",
                    "   #    #   ",
                    "            ",
                    "            ",
                    "            ",
                    "            ",
                    "   #    #   ",
                    "  #      #  ",
                ),
                (
                    "  #      #  ",
                    "            ",
                    "            ",
                    "            ",
                    "            ",
                    "            ",
                    "            ",
                    "  #      #  ",
                )
            )
        self.frame = 0
        self.size = [48, 32]
        self.color = (255, 150, 150)
        self.shape = pygame.Surface(self.size, SRCALPHA)  # pylint: disable=undefined-variable
        self.sprite = self.sprites[self.frame]

    def update(self):
        """
        description:
        """
        if self.update_timer.check():
            self.frame += 1
            if self.frame >= len(self.sprites):
                self.done = True
                return
            self.sprite = self.sprites[self.frame]
        draw(self.shape, self.sprite, self.color, 4)
        self.screen.blit(self.shape, self.position)


def draw(shape, sprite, tone, zoom, offset=None):
    """
    description:
    """
    if offset is None:
        offset = [0, 0]
    x_axis = offset[0]
    y_axis = offset[1]
    shape.fill((0, 0, 0))
    for i in sprite:
        for col in i:
            if col == "#":
                pygame.draw.rect(shape, tone, (x_axis, y_axis, zoom, zoom))
            x_axis += zoom
        y_axis += zoom
        x_axis = offset[0]
