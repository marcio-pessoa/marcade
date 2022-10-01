"""
---
name: joystick.py
description: Joystick package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *  # pylint: disable=wildcard-import, unused-import, unused-wildcard-import


class Joystick():
    """ Abstration class to manage joysticks with pygame. """

    def __init__(self):
        self.__enable = False
        self.__speed = 1
        self.__delay = 0
        self.__id = None
        self.joystick = None

    def identification(self, identification=None):
        """
        description: Identification control

        parameters:
          identification: Joystick ID (integer)

        returns:
          False: Initialization OK
          True: Initialization fails
          None: Not initialized
          int: Joystick ID
        """
        # Return current ID
        if identification is None:
            return self.__id
        # Check for valid ID
        if identification < 0 or identification > 10:
            return True
        # Set ID
        self.__id = identification
        try:
            pygame.joystick.init()
            self.joystick = pygame.joystick.Joystick(self.__id)
            self.joystick.init()
            self.enable()
            return False
        except AttributeError:
            if pygame.joystick.get_init():
                pygame.joystick.quit()
            self.__id = None
            return True

    def speed(self, speed=None):
        """
        description: Speed control

        parameters:
          speed: Speed factor

        return:
          False: Speed set successfully
          True: Speed set fails
          float: current speed factor
        """
        # Return current speed
        if speed is None:
            return self.__speed
        # Check for valid input
        if speed < 0 or speed > 100:
            return True
        # Set speed
        self.__speed = speed
        return False

    def delay(self, delay=None):
        """
        description: Delay control

        parameters:
          speed: Delay factor

        return:
          False: No error (Delay set successfully)
          True: Fail (Delay set fails)
          float: current delay factor
        """
        # Return current delay
        if delay is None:
            return self.__delay
        # Check for valid input
        if delay < 0 or delay > 100:
            return True
        # Set delay
        self.__delay = delay
        return False

    def enable(self):
        """
        description: Enable joystick

        parameters:
          None

        return:
          False: No errors (success)
          True: Errors found
        """
        if self.__id is None:
            return True
        self.__enable = True
        return False

    def disable(self):
        """
        description: Enable joystick

        parameters:
          None

        return:
          False: Always return False.
        """
        self.__enable = False
        return False

    def configuration(self):
        """
        description: Return joystick topology

        parameters:
          None

        return:
          True: If joystick was not initialized
          dict: Joystick configuration
        """
        if not self.__enable:
            return True
        config = \
            {
                'name': self.joystick.get_name(),
                'axes': self.joystick.get_numaxes(),
                'buttons': self.joystick.get_numbuttons(),
                'hats': self.joystick.get_numhats(),
                'balls': self.joystick.get_numballs()
            }
        return config

    def axis(self):
        """
        description: Axis position

        parameters:
          None

        return:
          dict: All axis positions
        """
        # Check if it's initialized
        if not self.__enable:
            return True
        axis = {}
        for i in range(self.joystick.get_numaxes()):
            axis = {**axis, i: self.joystick.get_axis(i)}
        return axis

    def hat(self):
        """
        description: Hat status

        parameters:
          None

        return:
          dict: Hat status
        """
        # Check if it's initialized
        if not self.__enable:
            return True
        hat = {}
        for i in range(self.joystick.get_numhats()):
            sensor = self.joystick.get_hat(i)
            hat = \
                {
                    **hat,
                    i: {
                        'x': sensor[0],
                        'y': sensor[1]
                    }
                }
        return hat

    def ball(self):
        """
        description: Ball status

        parameters:
          None

        return:
          dict: Ball status
        """
        # Check if it's initialized
        if not self.__enable:
            return True
        ball = {}
        for i in range(self.joystick.get_numballs()):
            ball = {**ball, i: self.joystick.get_ball(i)}
        return ball

    def button(self):
        """
        description: Button status

        parameters:
          None

        return:
          dict: Button status
        """
        # Check if it's initialized
        if not self.__enable:
            return True
        button = {}
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                button = {**button, i: True}
            else:
                button = {**button, i: False}
        return button

    def all(self):
        """
        description: Return all joystick axis, buttons, etc...

        parameters:
          None

        return:
          None: if not initialized
          dict: axis, button, hat and ball status
        """
        # Check if it's initialized
        if not self.__enable:
            return None
        return \
            {
                'axis': self.axis(),
                'button': self.button(),
                'hat': self.hat(),
                'ball': self.ball()
            }


def detect():
    """
    description: Detect joysticks

    parameters:
      None

    returns:
      False: If there is none joystick connected.
      tuple: With a list of joysticks IDs
    """
    pygame.joystick.init()
    count = pygame.joystick.get_count()
    # Create joystick list
    joystick_list = []
    for i in range(count):
        joystick_list.append(i)
    if count == 0:
        return False
    return tuple(joystick_list)
