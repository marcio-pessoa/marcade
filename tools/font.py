"""
---
name: font.py
description: Basic Font package file
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import pygame
from pygame.locals import SRCALPHA  # pylint: disable=no-name-in-module


class Font:  # pylint: disable=too-many-instance-attributes
    """
    description:
    """

    __version__ = 0.02

    def __init__(self, screen):
        self.screen = screen
        self.alphabet = (
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-"
        )
        self.sprites = (
            (
                "  #   ",
                " # #  ",
                "#   # ",
                "#   # ",
                "##### ",
                "#   # ",
                "#   # ",
            ), (
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
            ), (
                " ###  ",
                "#   # ",
                "#     ",
                "#     ",
                "#     ",
                "#   # ",
                " ###  ",
            ), (
                "####  ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "####  ",
            ), (
                "##### ",
                "#     ",
                "#     ",
                "####  ",
                "#     ",
                "#     ",
                "##### ",
            ), (
                "##### ",
                "#     ",
                "#     ",
                "####  ",
                "#     ",
                "#     ",
                "#     ",
            ), (
                " ###  ",
                "#   # ",
                "#     ",
                "#  ## ",
                "#   # ",
                "#   # ",
                " ###  ",
            ), (
                "#   # ",
                "#   # ",
                "#   # ",
                "##### ",
                "#   # ",
                "#   # ",
                "#   # ",
            ), (
                "##### ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "##### ",
            ), (
                "    # ",
                "    # ",
                "    # ",
                "    # ",
                "    # ",
                "#   # ",
                " ###  ",
            ), (
                "#   # ",
                "#  #  ",
                "# #   ",
                "###   ",
                "# #   ",
                "#  #  ",
                "#   # ",
            ), (
                "#     ",
                "#     ",
                "#     ",
                "#     ",
                "#     ",
                "#     ",
                "##### ",
            ), (
                "#   # ",
                "#   # ",
                "## ## ",
                "# # # ",
                "#   # ",
                "#   # ",
                "#   # ",
            ), (
                "#   # ",
                "#   # ",
                "##  # ",
                "# # # ",
                "#  ## ",
                "#   # ",
                "#   # ",
            ), (
                " ###  ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                " ###  ",
            ), (
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
                "#     ",
                "#     ",
                "#     ",
            ), (
                " ###  ",
                "#   # ",
                "#   # ",
                "#   # ",
                "# # # ",
                "#  #  ",
                " ## # ",
            ), (
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
                "# #   ",
                "#  #  ",
                "#   # ",
            ), (
                " ###  ",
                "#   # ",
                "#     ",
                " ###  ",
                "    # ",
                "#   # ",
                " ###  ",
            ), (
                "##### ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
            ), (
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                " ###  ",
            ), (
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                " # #  ",
                "  #   ",
            ), (
                "#   # ",
                "#   # ",
                "#   # ",
                "# # # ",
                "## ## ",
                "#   # ",
                "#   # ",
            ), (
                "#   # ",
                "#   # ",
                " # #  ",
                "  #   ",
                " # #  ",
                "#   # ",
                "#   # ",
            ), (
                "#   # ",
                "#   # ",
                "#   # ",
                " # #  ",
                "  #   ",
                "  #   ",
                "  #   ",
            ), (
                "##### ",
                "    # ",
                "   #  ",
                "  #   ",
                " #    ",
                "#     ",
                "##### ",
            ), (
                "       "
                "       "
                "       "
                "       "
                "       "
                "       "
                "       "
            ), (
                " ###  ",
                "#   # ",
                "#  ## ",
                "# # # ",
                "##  # ",
                "#   # ",
                " ###  ",
            ), (
                "  #   ",
                " ##   ",
                "# #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "##### ",
            ), (
                " ###  ",
                "#   # ",
                "   #  ",
                "  #   ",
                " #    ",
                "#     ",
                "##### ",
            ), (
                "####  ",
                "    # ",
                "    # ",
                " ###  ",
                "    # ",
                "    # ",
                "####  ",
            ), (
                "#     ",
                "#   # ",
                "#   # ",
                "##### ",
                "    # ",
                "    # ",
                "    # ",
            ), (
                "####  ",
                "#     ",
                "#     ",
                "####  ",
                "    # ",
                "    # ",
                "####  ",
            ), (
                " ###  ",
                "#     ",
                "#     ",
                "####  ",
                "#   # ",
                "#   # ",
                " ###  ",
            ), (
                "##### ",
                "    # ",
                "   #  ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
            ), (
                " ###  ",
                "#   # ",
                "#   # ",
                " ###  ",
                "#   # ",
                "#   # ",
                " ###  ",
            ), (
                " ###  ",
                "#   # ",
                "#   # ",
                " #### ",
                "    # ",
                "    # ",
                " ###  ",
            ), (
                "      ",
                "  #   ",
                "  #   ",
                "##### ",
                "  #   ",
                "  #   ",
                "      ",
            ), (
                "      ",
                "      ",
                "      ",
                "##### ",
                "      ",
                "      ",
                "      ",
            )
        )
        self.size = 1
        self.shape = None
        self.position = [0, 0]
        self.color = [200, 200, 200]

    def echo(self, string):
        """
        description:
        """
        position = list(self.position)
        for i in list(string):
            char = self.alphabet.index(i)
            sprite = self.sprites[char]
            size = (6 * self.__size, 7 * self.__size)
            self.shape = pygame.Surface(size, SRCALPHA)
            self.draw(sprite, (0, 0))
            self.screen.blit(self.shape, position)
            position[0] += self.__increment

    @property
    def size(self):
        """
        description:
        """
        return self.__size

    @size.setter
    def size(self, value):
        """
        description:
        """
        self.__size = value
        self.__increment = 6 * self.__size

    def set_position(self, position):
        """
        description:
        """
        self.position = position

    def set_color(self, color):
        """
        description:
        """
        self.color = color

    def draw(self, sprite, position):
        """
        description:
        """
        x_position = position[0]
        y_position = position[1]
        for row in sprite:
            for col in row:
                if col == "#":
                    pygame.draw.rect(self.shape, self.color,
                                     (x_position, y_position,
                                      self.__size, self.__size))
                x_position += self.__size
            y_position += self.__size
            x_position = position[0]
