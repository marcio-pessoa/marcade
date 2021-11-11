#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
name: marcade.py
description: Invasion package file
copyright: 2014-2020 Márcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
change-log: Check CHANGELOG.md file.
"""

try:
    import sys
    import argparse
    import os
    import logging
    import random
    import pygame
    from pygame.locals import \
    HWSURFACE, DOUBLEBUF, RESIZABLE, QUIT, KEYDOWN, K_ESCAPE, VIDEORESIZE, KEYUP
    import tools.joystick as joystick
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)


class MArcade():  # pylint: disable=too-many-instance-attributes
    """
    description:

    reference:
    - https://docs.python.org/2/library/argparse.html
      http://chase-seibert.github.io/blog/
    """

    __version__ = "0.3.4"

    def __init__(self):
        """
        https://docs.python.org/2/library/argparse.html
        http://chase-seibert.github.io/blog/
        """
        self.program_name = "marcade"
        self.program_date = "2020-01-08"
        self.program_description = "MArcade"
        self.program_copyright = "Copyright (c) 2014-2020 Marcio Pessoa"
        self.program_license = "GPLv2"
        self.program_website = "https://github.com/marcio-pessoa/marcade"
        self.program_contact = "Marcio Pessoa <marcio.pessoa@gmail.com>"
        self.window_title = self.program_description
        self.resizeable = False
        self.game = None
        self.available_games = ["invasion", "pongue", "rocks"]
        self.canvas_size = None
        self.clock = None
        self.joystick = None
        self.keys = None
        self.running = None
        self.screen = None
        self.screen_rate = None
        header = (
            'marcade <game> [<args>]\n\n' +
            'Games:\n' +
            '  invasion       based on memorable Space Invaders\n' +
            '  pongue         based on classic Pong\n' +
            '  rocks          based on amazing Asteroids\n\n')
        footer = (
            self.program_copyright + '\n' +
            'License: ' + self.program_license + '\n' +
            'Website: ' + self.program_website + '\n' +
            'Contact: ' + self.program_contact + '\n')
        examples = (
            'examples:\n' +
            '  marcade rocks\n' +
            '  marcade\n')
        self.version = (
            self.program_name + " " +
            str(self.__version__) + " (" +
            self.program_date + ")")
        epilog = (examples + '\n' + footer)
        parser = argparse.ArgumentParser(
            prog=self.program_name,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=epilog,
            add_help=True,
            usage=header)
        parser.add_argument('game', help='game to run')
        parser.add_argument(
            '-V', '--version',
            action='version',
            version=self.version,
            help='show version information and exit')
        if len(sys.argv) < 2:
            # Select a random game
            game = random.choice(self.available_games)
            eval("self." + str(game) + "()")  # pylint: disable=eval-used
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.game):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(True)
        getattr(self, args.game)()

    def __screen_start(self):
        self.running = True
        self.screen_rate = 60  # FPS
        self.canvas_size = (800, 480)  # WVGA (width, height) pixels
        self.__screen_set()
        self.__ctrl_set()

    def __screen_set(self):
        # Window position
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Initialise screen
        pygame.init()  # pylint: disable=no-member
        self.__screen_reset()
        # Window caption
        pygame.display.set_caption(self.window_title)
        # Clockling
        self.clock = pygame.time.Clock()

    def __screen_reset(self):
        if self.resizeable:
            self.screen = pygame.display.set_mode(
                self.canvas_size,
                HWSURFACE |
                DOUBLEBUF |
                RESIZABLE)
        else:
            self.screen = pygame.display.set_mode(
                self.canvas_size,
                HWSURFACE |
                DOUBLEBUF)

    def __run(self):
        while self.running:
            self.__check_event()
            self.game.run()
            self.clock.tick(self.screen_rate)
            pygame.display.flip()

    def __check_event(self):
        joy_state = None
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                self.keys.add(event.key)
            elif event.type == KEYUP:
                self.keys.remove(event.key)
            elif event.type == VIDEORESIZE:
                self.canvas_size = event.dict['size']
                self.__screen_reset()
                self.game.size_reset()
        joy_state = self.joystick.all()
        self.game.control(self.keys, joy_state)

    def __ctrl_set(self):
        # Set keyboard speed
        pygame.key.set_repeat(0, 0)
        self.keys = set()
        self.joystick = joystick.Joystick()
        if joystick.detect():
            self.joystick.identification(joystick.detect()[0])
            print(self.joystick.configuration())

    def pongue(self):
        """
        description:
        """
        from games.pongue import Pongue  # pylint: disable=import-outside-toplevel
        parser = argparse.ArgumentParser(
            prog=self.program_name + ' pongue',
            description='based on classic Pong')
        parser.add_argument(
            '-v', '--verbosity',
            type=str,
            default='ERROR',
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
            help='verbose mode, options: ' +
            'CRITICAL, ERROR (default), WARNING, INFO, DEBUG')
        args = parser.parse_args(sys.argv[2:])
        verbosity(args.verbosity)
        self.window_title = 'Pongue'
        game_start_message(self.window_title, Pongue.__version__)
        self.resizeable = True
        self.__screen_start()
        self.game = Pongue(self.screen)
        self.__run()
        sys.exit(False)

    def rocks(self):
        """
        description:
        """
        from games.rocks import Rocks  # pylint: disable=import-outside-toplevel
        parser = argparse.ArgumentParser(
            prog=self.program_name + ' rocks',
            description='based on amazing Asteroids')
        parser.add_argument(
            '-v', '--verbosity',
            type=str,
            default='ERROR',
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
            help='verbose mode, options: ' +
            'CRITICAL, ERROR (default), WARNING, INFO, DEBUG')
        args = parser.parse_args(sys.argv[2:])
        verbosity(args.verbosity)
        self.window_title = 'Rocks'
        game_start_message(self.window_title, Rocks.__version__)
        self.__screen_start()
        self.game = Rocks(self.screen)
        self.__run()
        sys.exit(False)

    def invasion(self):
        """
        description:
        """
        from games.invasion import Invasion  # pylint: disable=import-outside-toplevel
        parser = argparse.ArgumentParser(
            prog=self.program_name + ' invasion',
            description='based on Space Invaders')
        parser.add_argument(
            '-v', '--verbosity',
            type=str,
            default='ERROR',
            choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
            help='verbose mode, options: ' +
            'CRITICAL, ERROR (default), WARNING, INFO, DEBUG')
        args = parser.parse_args(sys.argv[2:])
        verbosity(args.verbosity)
        self.window_title = 'Invasion'
        game_start_message(self.window_title, Invasion.__version__)
        self.__screen_start()
        self.game = Invasion(self.screen)
        self.__run()
        sys.exit(False)


def verbosity(level):
    """
    description:
    """
    if level == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    elif level == 'INFO':
        logging.basicConfig(level=logging.INFO)
    elif level == 'WARNING':
        logging.basicConfig(level=logging.WARNING)
    elif level == 'ERROR':
        logging.basicConfig(level=logging.ERROR)
    elif level == 'CRITICAL':
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.ERROR)

def game_start_message(name, version):
    """
    description:
    """
    logging.info("Starting %s version %s", name, version)

def main():
    """
    description:
    """
    MArcade()


if __name__ == '__main__':
    main()
