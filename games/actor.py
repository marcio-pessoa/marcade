"""
---
name: actor.py
description: Actor file
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import pygame
from pygame.locals import SRCALPHA
from src.timer import Timer


class Ship:
    """ Ship class """

    __move_increment = 5
    __size = [48, 32]
    __sprite = (
        "            ",
        "     ##     ",
        "    ####    ",
        "   ######   ",
        " ########## ",
        "  ########  ",
        " ########## ",
        "############",
    )

    def __init__(self, screen):
        self.__screen = screen
        self.enable = True
        self.reset()
        self.shape = pygame.Surface(self.__size, SRCALPHA)
        self.radius = self.shape.get_rect().center[0]
        self.rect = self.shape.get_rect().move(self.position)
        _draw(self.shape, self.__sprite, (180, 180, 240), 4)

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


class Missile:  # pylint: disable=too-few-public-methods
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
        color = self.__color[self.__aspect]
        _draw(self.__shape, self.__aliens[self.__aspect][self.pose], color, 4)
        self.rect = self.__shape.get_rect().move(self.position)
        self.__screen.blit(self.__shape, self.position)

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
        self.pose = (self.pose + 1) % 2
        self.update()


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
        self.rect = self.shape.get_rect().move(self.position)
        self.update()

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
