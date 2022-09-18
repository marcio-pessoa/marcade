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
        self.screen_size = [self.screen.get_size()[0], self.screen.get_size()[1]]

    @abstractmethod
    def run(self):
        """ Run game """

    @abstractmethod
    def control(self):
        """ Get user control input """
