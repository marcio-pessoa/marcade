"""
---
name: game_manager.py
description: Game Manager package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

from games.invasion import Invasion
from games.pongue import Pongue
from games.rocks import Rocks
from games.serpent import Serpent
from games.m2048 import M2048


class GameManager:
    """ Game Manager class """

    def __init__(self):
        self.games = {
            'invasion': Invasion,
            'pongue': Pongue,
            'rocks': Rocks,
            'serpent': Serpent,
            '2048': M2048
        }

    def get_games(self):
        """ Get all games """
        return self.games

    def get_game(self, name):
        """ Get a game by name """
        return self.games.get(name)
