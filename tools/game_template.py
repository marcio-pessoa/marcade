"""
---
name: game_template.py
description: Game Template Class
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import sys
from abc import ABC, abstractmethod
import pygame
try:
    from pygame.locals import SRCALPHA
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)


class Game(ABC):
    """ Generic game class

    Args:
        ABC (Abstract class): Abstract class for Template Method
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.screen_size = [
            self.screen.get_size()[0], self.screen.get_size()[1]
        ]
        self.canvas = pygame.Surface(self.screen_size, SRCALPHA, 32)
        self.canvas.convert_alpha()

    @abstractmethod
    def control(self, keys, joystick) -> None:
        """ Receive control commands

        Args:
            keys (_type_): Keyboard commands
            joystick (_type_): Joystick commands
        """

    @abstractmethod
    def update(self) -> None:
        """ Update game match """

    @abstractmethod
    def start(self) -> None:
        """ Start game match """

    @abstractmethod
    def reset(self) -> None:
        """ Restart game match """

    def stop(self) -> None:
        """ Stop game match """
        pygame.event.clear()
