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

from tools import game
from tools.log import Log


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
            add_help=True,
            usage=(
                'marcade <game> [<args>]\n\n' +
                'Games:\n' +
                '  invasion       based on memorable Space Invaders\n' +
                '  pongue         based on classic Pong\n' +
                '  rocks          based on amazing Asteroids\n\n')
            )
        parser.add_argument('game', help='game to run')
        parser.add_argument(
            '-V', '--version',
            action='version',
            version=(
                f'{self.program_name} '
                f'{self.__version__} ('
                f'{self.program_date})'
            ),
            help='show version information and exit')
        if len(sys.argv) < 2:
            # Select a random game
            run = random.choice(self.available_games)
            eval("self." + str(run) + "()")  # pylint: disable=eval-used
            sys.exit()
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.game):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(True)
        getattr(self, args.game)()

    def pongue(self):
        """
        description:
        """
        from games.pongue import Pongue  # pylint: disable=import-outside-toplevel
        title = 'Pongue'
        parser = argparse.ArgumentParser(
            prog=f'{self.program_name} {title}',
            description='based on classic Pong')
        parser.add_argument(
            '-v', '--verbosity',
            type=str,
            default='ERROR',
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
            help='verbose mode, options: ' +
            'CRITICAL, ERROR (default), WARNING, INFO, DEBUG')
        args = parser.parse_args(sys.argv[2:])
        Log().verbosity = args.verbosity
        game.Game(Pongue).run()

    def rocks(self):
        """
        description:
        """
        from games.rocks import Rocks  # pylint: disable=import-outside-toplevel
        title = 'Rocks'
        parser = argparse.ArgumentParser(
            prog=f'{self.program_name} {title}',
            description='based on amazing Asteroids')
        parser.add_argument(
            '-v', '--verbosity',
            type=str,
            default='ERROR',
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
            help='verbose mode, options: ' +
            'CRITICAL, ERROR (default), WARNING, INFO, DEBUG')
        args = parser.parse_args(sys.argv[2:])
        Log().verbosity = args.verbosity
        game.Game(Rocks).run()

    def invasion(self):
        """
        description:
        """
        from games.invasion import Invasion  # pylint: disable=import-outside-toplevel
        title = 'Invasion'
        parser = argparse.ArgumentParser(
            prog=f'{self.program_name} {title}',
            description='based on Space Invaders')
        parser.add_argument(
            '-v', '--verbosity',
            type=str,
            default='ERROR',
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
            help='verbose mode, options: ' +
            'CRITICAL, ERROR (default), WARNING, INFO, DEBUG')
        args = parser.parse_args(sys.argv[2:])
        Log().verbosity = args.verbosity
        game.Game(Invasion).run()


if __name__ == '__main__':
    MArcade()
