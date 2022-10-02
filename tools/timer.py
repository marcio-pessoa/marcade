"""
---
name: timer.py
description: Timer package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import time


class Timer:
    """
    description:
    """

    def __init__(self, period: float, style: str = "LOOP"):
        self.millis = lambda: int(round(time.time() * 1000))
        self.__period = period
        self.__style = style
        self.__enable = True
        self.counter = self.millis()

    @property
    def period(self):
        """
        description:
        """
        return self.__period

    @period.setter
    def period(self, value: float):
        """
        description:
        """
        self.__period = value
        self.reset()

    def reset(self):
        """
        description:
        """
        self.counter = self.millis()

    def enable(self):
        """
        description:
        """
        self.__enable = True

    def disable(self):
        """
        description:
        """
        self.__enable = False

    def check(self):
        """
        description:
        """
        if not self.__enable:
            return False
        if self.__style == "LOOP":
            if self.millis() - self.counter >= self.__period:
                self.counter = self.millis()
                return True
        if self.__style == "COUNTDOWN":
            if self.millis() - self.counter >= self.__period:
                self.__enable = False
                return True
        if self.__style == "STOPWATCH":
            return self.millis() - self.counter
        return False

    def status(self):
        """
        description:
        """
        return self.millis() - self.counter
