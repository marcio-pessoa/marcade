#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
name: marcade.py
description: Invasion package file
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import sys
import random
import argparse

from tools.log import Log
from tools.arcade import Arcade
from games.invasion import Invasion
from games.pongue import Pongue
from games.rocks import Rocks


class MArcade():
    """
    MArcade class

    argparse reference:
      - https://docs.python.org/2/library/argparse.html
      - http://chase-seibert.github.io/blog/
    """

    __version__ = '0.3.4'

    def __init__(self):
        self.program_name = "marcade"
        self.program_date = "2022-09-18"
        self.program_description = "MArcade"
        self.available_games = ["invasion", "pongue", "rocks"]

        Log().name = self.program_name
        Log().verbosity = 'ERROR'

        parser = argparse.ArgumentParser(
            prog=self.program_name,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=True,
            usage=(
                'marcade <game> [<args>]\n\n' +
                'Games:\n' +
                '  invasion       based on memorable Space Invaders\n' +
                '  pongue         based on classic Pong\n' +
                '  rocks          based on amazing Asteroids\n\n'
            ),
            epilog=(
                'examples:\n'
                '  marcade rocks\n'
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
            version=(
                f'{self.program_name} {self.__version__} {self.program_date})'
            ),
        )

        if len(sys.argv) < 2:  # No args given, select a random game
            run = random.choice(self.available_games)
            eval("self." + str(run) + "()")  # pylint: disable=eval-used
            sys.exit()

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.game):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(True)

        getattr(self, args.game)()

    @staticmethod
    def __common_arguments(func):
        """
        description:
        """
        def wrapper():
            parser = argparse.ArgumentParser()
            parser.add_argument(
                '-v', '--verbosity',
                type=str,
                default='ERROR',
                choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
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
    def invasion(_description: str = 'memorable Space Invaders'):
        """ Invasion """
        Arcade(Invasion).run()


if __name__ == '__main__':
    MArcade()
