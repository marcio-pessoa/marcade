"""
---
name: game_template.py
description: Game Template Class
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

from abc import ABC, abstractmethod
import pygame


class Game(ABC):
    """ Generic game class """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.screen_size = [
            self.screen.get_size()[0], self.screen.get_size()[1]
        ]

    @abstractmethod
    def control(self, keys, joystick) -> None:
        """ Receive control commands

        Args:
            keys (_type_): Keyboard commands
            joystick (_type_): Joystick commands
        """

    @abstractmethod
    def update(self) -> None:
        """ Update game """

    def stop(self) -> None:
        """ Stop game """
        pygame.event.clear()
