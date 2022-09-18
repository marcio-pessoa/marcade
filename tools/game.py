"""
---
name: game.py
description: Pygame
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import os
import sys
try:
    import pygame
    from pygame.locals import \
    HWSURFACE, DOUBLEBUF, QUIT, KEYDOWN, K_ESCAPE, KEYUP
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)

from tools import joystick
from tools.log import log


SCREEN_RATE = 60  # FPS


class Game():
    """ Game class """

    def __init__(self, game_class) -> None:
        self.__game_class = game_class
        log.info("Starting %s version %s",
            self.__game_class.__name__,
            self.__game_class.__version__)
        # Window position
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()  # pylint: disable=no-member
        pygame.display.set_caption(self.__game_class.__name__)
        self.screen_reset()
        self.clock = pygame.time.Clock()
        self.running = True
        self.__ctrl_set()

    def run(self, ) -> None:
        """ Run game

        Args:
            game (function): The desired game running method
        """
        game = self.__game_class(self.screen)
        while self.running:
            keyboard, joypad = self.__check_event()
            game.control(keyboard, joypad)
            game.run()
            self.clock.tick(SCREEN_RATE)
            pygame.display.flip()

    def screen_reset(self) -> None:
        """ Reset screens to default values """
        canvas_size = (800, 480)  # WVGA
        self.screen = pygame.display.set_mode(
            canvas_size,
            HWSURFACE |
            DOUBLEBUF)

    def __ctrl_set(self):
        # Set keyboard speed
        pygame.key.set_repeat(0, 0)
        self.keys = set()
        self.joystick = joystick.Joystick()
        if joystick.detect():
            self.joystick.identification(joystick.detect()[0])
            print(self.joystick.configuration())

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
        joy_state = self.joystick.all()
        return self.keys, joy_state
