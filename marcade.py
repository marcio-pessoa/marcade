#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
name: marcade.py
description: MArcade main file
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import sys
import random
import argparse

from src.log import Log
from src.arcade import Arcade
from src.game_manager import GameManager


class MArcade():  # pylint: disable=too-few-public-methods
    """ MArcade class """

    __version__ = '0.5.0'
    __date__ = "2025-12-02"

    def __init__(self):
        Log().name = 'marcade'
        Log().verbosity = 'WARNING'
        Log().start()

        parser = argparse.ArgumentParser(
            prog='marcade',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=True,
            usage=(
                'marcade <game> [<args>]\n\n'
                'Games:\n'
                '  2048           based on the addictive 2048\n'
                '  invasion       based on memorable Space Invaders\n'
                '  pongue         based on classic Pong\n'
                '  serpent        based on the fun Snake\n'
                '  pacguy         based on the classic Pac-Man\n\n'
                '  rocks          based on amazing Asteroids\n'
            ),
            epilog=(
                'examples:\n'
                '  marcade invasion\n'
                '  marcade\n'
                '\n'
                'Copyleft (c) 2014-2025 Marcio Pessoa\n'
                'License: GPLv2\n'
                'Website: https://github.com/marcio-pessoa/marcade\n'
                'Contact: Marcio Pessoa <marcio.pessoa@gmail.com>\n'
            ),
        )
        parser.add_argument('game', help='game to run')
        parser.add_argument(
            '-V', '--version',
            action='version',
            help='show version information and exit',
            version=(f'MArcade {self.__version__} {self.__date__}'),
        )

        game_manager = GameManager()
        games = game_manager.get_games()

        if len(sys.argv) < 2:  # When no args given, run random game
            game_name = random.choice(list(games.keys()))  # nosec
            self.run_game(games[game_name])
            sys.exit()

        args = parser.parse_args(sys.argv[1:2])
        game = game_manager.get_game(args.game)

        if not game:
            print('Unrecognized command')
            parser.print_help()
            sys.exit(True)

        self.run_game(game)

    def run_game(self, game):
        """ Run a game """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-v', '--verbosity',
            type=str,
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
            default='ERROR',
            help=(
                'verbose mode, options: '
                'CRITICAL, ERROR (default), WARNING, INFO, DEBUG'
            )
        )
        args = parser.parse_args(sys.argv[2:])
        Log().verbosity = args.verbosity
        Arcade(game).run()


if __name__ == '__main__':
    MArcade()
