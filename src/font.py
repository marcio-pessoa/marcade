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


class Font:
    """ A basic font class """

    def __init__(self, screen):
        self.screen = screen
        self.chars = {
            'A': (
                "  #   ",
                " # #  ",
                "#   # ",
                "#   # ",
                "##### ",
                "#   # ",
                "#   # ",
            ),
            'B': (
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
            ),
            'C': (
                " ###  ",
                "#   # ",
                "#     ",
                "#     ",
                "#     ",
                "#   # ",
                " ###  ",
            ),
            'D': (
                "####  ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "####  ",
            ),
            'E': (
                "##### ",
                "#     ",
                "#     ",
                "####  ",
                "#     ",
                "#     ",
                "##### ",
            ),
            'F': (
                "##### ",
                "#     ",
                "#     ",
                "####  ",
                "#     ",
                "#     ",
                "#     ",
            ),
            'G': (
                " ###  ",
                "#   # ",
                "#     ",
                "#  ## ",
                "#   # ",
                "#   # ",
                " ###  ",
            ),
            'H': (
                "#   # ",
                "#   # ",
                "#   # ",
                "##### ",
                "#   # ",
                "#   # ",
                "#   # ",
            ),
            'I': (
                "##### ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "##### ",
            ),
            'J': (
                "    # ",
                "    # ",
                "    # ",
                "    # ",
                "    # ",
                "#   # ",
                " ###  ",
            ),
            'K': (
                "#   # ",
                "#  #  ",
                "# #   ",
                "###   ",
                "# #   ",
                "#  #  ",
                "#   # ",
            ),
            'L': (
                "#     ",
                "#     ",
                "#     ",
                "#     ",
                "#     ",
                "#     ",
                "##### ",
            ),
            'M': (
                "#   # ",
                "#   # ",
                "## ## ",
                "# # # ",
                "#   # ",
                "#   # ",
                "#   # ",
            ),
            'N': (
                "#   # ",
                "#   # ",
                "##  # ",
                "# # # ",
                "#  ## ",
                "#   # ",
                "#   # ",
            ),
            'O': (
                " ###  ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                " ###  ",
            ),
            'P': (
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
                "#     ",
                "#     ",
                "#     ",
            ),
            'Q': (
                " ###  ",
                "#   # ",
                "#   # ",
                "#   # ",
                "# # # ",
                "#  #  ",
                " ## # ",
            ),
            'R': (
                "####  ",
                "#   # ",
                "#   # ",
                "####  ",
                "# #   ",
                "#  #  ",
                "#   # ",
            ),
            'S': (
                " ###  ",
                "#   # ",
                "#     ",
                " ###  ",
                "    # ",
                "#   # ",
                " ###  ",
            ),
            'T': (
                "##### ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
            ),
            'U': (
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                " ###  ",
            ),
            'V': (
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                "#   # ",
                " # #  ",
                "  #   ",
            ),
            'W': (
                "#   # ",
                "#   # ",
                "#   # ",
                "# # # ",
                "## ## ",
                "#   # ",
                "#   # ",
            ),
            'X': (
                "#   # ",
                "#   # ",
                " # #  ",
                "  #   ",
                " # #  ",
                "#   # ",
                "#   # ",
            ),
            'Y': (
                "#   # ",
                "#   # ",
                "#   # ",
                " # #  ",
                "  #   ",
                "  #   ",
                "  #   ",
            ),
            'Z': (
                "##### ",
                "    # ",
                "   #  ",
                "  #   ",
                " #    ",
                "#     ",
                "##### ",
            ),
            ' ': (
                "       "
                "       "
                "       "
                "       "
                "       "
                "       "
                "       "
            ),
            '0': (
                " ###  ",
                "#   # ",
                "#  ## ",
                "# # # ",
                "##  # ",
                "#   # ",
                " ###  ",
            ),
            '1': (
                "  #   ",
                " ##   ",
                "# #   ",
                "  #   ",
                "  #   ",
                "  #   ",
                "##### ",
            ),
            '2': (
                " ###  ",
                "#   # ",
                "   #  ",
                "  #   ",
                " #    ",
                "#     ",
                "##### ",
            ),
            '3': (
                "####  ",
                "    # ",
                "    # ",
                " ###  ",
                "    # ",
                "    # ",
                "####  ",
            ),
            '4': (
                "#     ",
                "#   # ",
                "#   # ",
                "##### ",
                "    # ",
                "    # ",
                "    # ",
            ),
            '5': (
                "####  ",
                "#     ",
                "#     ",
                "####  ",
                "    # ",
                "    # ",
                "####  ",
            ),
            '6': (
                " ###  ",
                "#     ",
                "#     ",
                "####  ",
                "#   # ",
                "#   # ",
                " ###  ",
            ),
            '7': (
                "##### ",
                "    # ",
                "   #  ",
                "  #   ",
                "  #   ",
                "  #   ",
                "  #   ",
            ),
            '8': (
                " ###  ",
                "#   # ",
                "#   # ",
                " ###  ",
                "#   # ",
                "#   # ",
                " ###  ",
            ),
            '9': (
                " ###  ",
                "#   # ",
                "#   # ",
                " #### ",
                "    # ",
                "    # ",
                " ###  ",
            ),
            '+': (
                "      ",
                "  #   ",
                "  #   ",
                "##### ",
                "  #   ",
                "  #   ",
                "      ",
            ),
            '-': (
                "      ",
                "      ",
                "      ",
                "##### ",
                "      ",
                "      ",
                "      ",
            )

        }
        self.size = 1
        self.shape = None
        self.position = [0, 0]
        self.color = [200, 200, 200]

    def echo(self, string: str):
        """ echo desired string """
        position = list(self.position)
        for i in list(string):
            sprite = self.chars[i]
            size = (6 * self.size, 7 * self.size)
            self.shape = pygame.Surface(size, SRCALPHA)
            self.draw(sprite, (0, 0))
            self.screen.blit(self.shape, position)
            position[0] += 6 * self.size

    def draw(self, sprite, position):
        """ draw current char """
        x_position = position[0]
        y_position = position[1]
        for row in sprite:
            for col in row:
                if col == "#":
                    pygame.draw.rect(
                        self.shape, self.color,
                        (x_position, y_position, self.size, self.size)
                    )
                x_position += self.size
            y_position += self.size
            x_position = position[0]
