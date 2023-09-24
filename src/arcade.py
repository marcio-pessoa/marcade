"""
---
name: ambience.py
description: Ambience PyGame
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import os
import sys
import contextlib
try:
    with contextlib.redirect_stdout(None):
        import pygame
    from pygame.locals import DOUBLEBUF, QUIT, KEYDOWN, K_ESCAPE, KEYUP
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)

from src import joystick
from src.log import log
from src.game_template import Game


RATE = 60  # FPS
SIZE = (800, 480)  # WVGA


class Arcade():
    """ Ambience class

    Args:
        game (class): The desired game class
    """

    def __init__(self, game_class: Game) -> None:
        self.__game_class = game_class
        log.info(
            "Starting %s version %s",
            self.__game_class.__name__, self.__game_class.__version__
        )
        self.__running = False
        self.__screen_start()
        self.__control_start()

    @property
    def running(self) -> bool:
        """ running getter

        Returns:
            bool: True if game is running
        """
        return self.__running

    def run(self) -> None:
        """ Run game """
        self.__running = True
        game: Game = self.__game_class(self.__screen)
        while self.__running:
            keyboard, joypad = self.__check_event()
            game.control(keyboard, joypad)
            game.update()
            self.__clock.tick(RATE)
            pygame.display.flip()
        log.debug('Finished.')

    def __screen_start(self) -> None:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()  # pylint: disable=no-member
        pygame.display.set_caption(self.__game_class.__name__)
        self.__screen = pygame.display.set_mode(SIZE, DOUBLEBUF)
        self.__clock = pygame.time.Clock()

    def __control_start(self) -> None:
        pygame.key.set_repeat(0, 0)  # Set keyboard speed
        self.keys = set()
        self.joystick = joystick.Joystick()
        if joystick.detect():
            self.joystick.identification(joystick.detect()[0])
            print(self.joystick.configuration())

    def __check_event(self):
        joy_state = None
        for event in pygame.event.get():
            if event.type == QUIT:
                self.__running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__running = False
                self.keys.add(event.key)
            elif event.type == KEYUP:
                self.keys.remove(event.key)
        joy_state = self.joystick.all()
        return self.keys, joy_state
