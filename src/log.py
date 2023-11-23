"""
---
name: log.py
description: Log package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import sys
import logging
import logging.handlers


class Log:
    """ Log Borg pattern """
    _shared_state = {}
    name: str = 'Default log'
    logger = logging.getLogger(name)
    __verbosity: int = logging.WARNING  # example: logging.ERROR

    def __new__(cls):
        inst = super().__new__(cls)
        inst.__dict__ = cls._shared_state
        return inst

    def start(self) -> None:
        """ Start the log system """
        fmt = self.name + ' [%(process)d]: %(levelname)s: %(message)s'
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter(fmt))
        self.logger.addHandler(handler)

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

        self.logger.setLevel(self.__verbosity)


class CustomFormatter(logging.Formatter):
    """ Add colors to log """
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.formats = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log = Log().logger
