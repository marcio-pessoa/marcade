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
    from pygame.locals import SRCALPHA, K_ESCAPE, K_RIGHT, K_LEFT, K_SPACE, \
        K_a, K_RETURN
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)

from tools.font import Font
from tools.sound import Sound
from tools.timer import Timer
from tools.game_template import Game


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
            self._game_over()

    def _collision_check(self):  # pylint: disable=too-many-branches
        # Ship Missle against Alien
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
        # Alien Missle againt Ship
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
            if i.is_out():
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
            i.update()
            if random.randrange(self.alien_burst_seed) == 1:
                shoot = Missile(self.canvas, i.position, 4, -1)
                self.alien_burst.add(shoot)
                break

    def _game_over(self):
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


class Ship:
    """ Ship class """

    __move_increment = 5
    __size = [48, 32]

    def __init__(self, screen):
        self.__screen = screen
        self.enable = True
        sprite = (
            "            ",
            "     ##     ",
            "    ####    ",
            "   ######   ",
            " ########## ",
            "  ########  ",
            " ########## ",
            "############",
        )
        self.reset()
        self.shape = pygame.Surface(self.__size, SRCALPHA)
        _draw(self.shape, sprite, (180, 180, 240), 4)
        self.radius = self.shape.get_rect().center[0]
        self.rect = self.shape.get_rect().move(self.position)

    def reset(self):
        """
        description:
        """
        screen_size = [
            self.__screen.get_size()[0],
            self.__screen.get_size()[1]
        ]
        self.position = [screen_size[0] / 2, screen_size[1] - self.__size[1]]
        self.enable = True

    def update(self):
        """
        description:
        """
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[0] + self.__size[0] > self.__screen.get_size()[0]:
            self.position[0] = self.__screen.get_size()[0] - self.__size[0]
        self.rect = self.shape.get_rect().move(self.position)
        self.__screen.blit(self.shape, self.position)

    def move_right(self):
        """
        description:
        """
        if self.enable:
            self.position[0] += self.__move_increment

    def move_left(self):
        """
        description:
        """
        if self.enable:
            self.position[0] -= self.__move_increment


class Missile:
    """ Missile class """

    __sprite = (
        "##",
        "##",
        "##",
        "##",
    )
    __size = [8, 16]
    __radius = 24

    def __init__(self, screen, ship_position, speed, direction=1):
        self.screen = screen
        self.out = False
        self.speed = speed * direction
        self.shape = pygame.Surface(self.__size, SRCALPHA)
        self.enable = True
        self.position = self._position_calc(ship_position, direction)
        _draw(self.shape, self.__sprite, (250, 250, 250), 4)
        self.update()

    def _position_calc(self, ship_position, direction):
        position = [0, 0]
        position[0] = ship_position[0] + self.__radius - self.__size[0] / 2
        if direction == 1:
            position[1] = ship_position[1] - self.__size[1]
        elif direction == -1:
            position[1] = ship_position[1] + self.__size[1] + 20
        return position

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


class Monster:
    """ Monster class """
    __aliens = (
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
    __color = (
        (150, 200, 100),
        (200, 200, 100),
        (100, 200, 200),
        (200, 100, 200),
        (100, 100, 200),
        (200, 100, 100)
    )
    size = [48, 32]

    def __init__(self, screen, aspect, position):
        self.__shape = pygame.Surface(self.size, SRCALPHA)
        self.__screen = screen
        self.__aspect = aspect % 6
        self.position = position
        self.pose = 0
        self.enable = True

        color = self.__color[self.__aspect]
        _draw(self.__shape, self.__aliens[self.__aspect][self.pose], color, 4)
        self.update()

    @property
    def points(self) -> int:
        """ Points per monster getter

        Returns:
            int: Monster points
        """
        return 10 - self.__aspect

    def update(self):
        """ Update shape and position """
        self.rect = self.__shape.get_rect().move(self.position)
        self.__screen.blit(self.__shape, self.position)

    def march(self, way, drop):
        """
        description:
        """
        color = self.__color[self.__aspect]
        if not self.enable:
            return
        if way:
            increment = 1
        else:
            increment = -1
        self.position[0] += increment * 4
        if drop:
            self.position[1] += increment * 16
        _draw(self.__shape, self.__aliens[self.__aspect][self.pose], color, 4)
        self.pose = (self.pose + 1) % 2


class Barrier:
    """ Barrier class """

    __color = (139, 105, 20)
    __sprites = (
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
    points = 1

    def __init__(self, screen, position):
        self.__screen = screen
        self.position = position
        self.status = len(self.__sprites) - 1
        self.shape = pygame.Surface([48, 32], SRCALPHA)
        _draw(self.shape, self.__sprites[self.status], self.__color, 4)
        self.rect = self.shape.get_rect().move(self.position)

    def update(self):
        """
        description:
        """
        _draw(self.shape, self.__sprites[self.status], self.__color, 4)
        self.__screen.blit(self.shape, self.position)

    def add_damage(self):
        """
        description:
        """
        self.status -= 1
        _draw(self.shape, self.__sprites[self.status], self.__color, 4)
        return self.status


class Explosion:  # pylint: disable=too-few-public-methods
    """ Explosion class """

    __sprites = (
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

    def __init__(self, screen, position):
        self.__screen = screen
        self.__position = position
        self.__update_timer = Timer(50)
        self.__frame = 0
        self.done = False

    def update(self):
        """
        description:
        """
        shape = pygame.Surface([48, 32], SRCALPHA)
        sprite = self.__sprites[self.__frame]

        if self.__update_timer.check():
            self.__frame += 1
            if self.__frame >= len(self.__sprites):
                self.done = True
                return
            sprite = self.__sprites[self.__frame]

        _draw(shape, sprite, (255, 150, 150), 4)
        self.__screen.blit(shape, self.__position)


def _draw(shape, sprite, tone, zoom, offset=None):
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
