"""
---
name: log.py
description: Log Singleton package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import sys
import logging
import logging.handlers


class Log:
    """ Log Singleton """
    name: str = 'Default log'
    logger = logging.getLogger(name)
    __verbosity: int = logging.INFO  # example: logging.ERROR

    def __new__(cls):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def start(self) -> None:
        """ Start log system """
        formatter = logging.Formatter(
            fmt=self.name + ' [%(process)d]: %(levelname)s: %(message)s'
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(self.__verbosity)

    @property
    def verbosity(self) -> int:
        """ verbosity getter function

        Returns:
            int: verbosity level
        """
        return self.__verbosity

    @verbosity.setter
    def verbosity(self, level):
        if level == 'DEBUG':
            self.__verbosity = logging.DEBUG
        elif level == 'INFO':
            self.__verbosity = logging.INFO
        elif level == 'WARNING':
            self.__verbosity = logging.WARNING
        elif level == 'ERROR':
            self.__verbosity = logging.ERROR
        elif level == 'CRITICAL':
            self.__verbosity = logging.CRITICAL
        else:
            self.__verbosity = logging.ERROR
        self.start()


log = Log().logger
