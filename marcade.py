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
from games.invasion import Invasion
from games.pongue import Pongue
from games.rocks import Rocks
from games.serpent import Serpent


class MArcade():
    """ MArcade class """

    __version__ = '0.4.0'
    __date__ = "2022-10-17"

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
                '  invasion       based on memorable Space Invaders\n'
                '  pongue         based on classic Pong\n'
                '  serpent        based on the fun Snake\n'
                '  rocks          based on amazing Asteroids\n\n'
            ),
            epilog=(
                'examples:\n'
                '  marcade invasion\n'
                '  marcade\n'
                '\n'
                'Copyleft (c) 2014-2022 Marcio Pessoa\n'
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

        if len(sys.argv) < 2:  # When no args given, run random game
            game = random.choice(['invasion', 'pongue', 'rocks', 'serpent'])
            getattr(self, game)()
            sys.exit()

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.game):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(True)

        getattr(self, args.game)()

    @staticmethod
    def __common_arguments(func):
        def wrapper():
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
            func()
        return wrapper

    @staticmethod
    @__common_arguments
    def invasion():
        """ Invasion """
        Arcade(Invasion).run()

    @staticmethod
    @__common_arguments
    def pongue():
        """ Pongue """
        Arcade(Pongue).run()

    @staticmethod
    @__common_arguments
    def rocks():
        """ Rocks """
        Arcade(Rocks).run()

    @staticmethod
    @__common_arguments
    def serpent():
        """ Serpent """
        Arcade(Serpent).run()


if __name__ == '__main__':
    MArcade()
