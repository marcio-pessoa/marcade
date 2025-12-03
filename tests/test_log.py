"""
---
name: test_log.py
description: Test Log Class
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
import logging as real_logging
from unittest.mock import MagicMock, patch
import sys

# pylint: disable=protected-access


class TestLog(unittest.TestCase):
    """ Test Log Class """

    @classmethod
    def setUpClass(cls):
        """ Set up class patches """
        cls.mock_logging = MagicMock()
        cls.mock_logging.handlers = MagicMock()

        # Set real logging levels on the mock
        cls.mock_logging.DEBUG = real_logging.DEBUG
        cls.mock_logging.INFO = real_logging.INFO
        cls.mock_logging.WARNING = real_logging.WARNING
        cls.mock_logging.ERROR = real_logging.ERROR
        cls.mock_logging.CRITICAL = real_logging.CRITICAL

        cls.modules_patcher = patch.dict(sys.modules, {
            'logging': cls.mock_logging,
            'logging.handlers': cls.mock_logging.handlers,
        })
        cls.modules_patcher.start()

        # pylint: disable=import-outside-toplevel
        from src.log import Log
        cls.Log = Log

    @classmethod
    def tearDownClass(cls):
        """ Tear down class patches """
        cls.modules_patcher.stop()

    def setUp(self):
        """ Set up test """
        # Because Log is a Borg, we need to reset its state for each test
        self.Log._shared_state = {}
        self.log = self.Log()
        self.log.logger = self.mock_logging.getLogger()

    def test_initialization(self):
        """ Test initialization """
        self.assertEqual(self.log.verbosity, real_logging.WARNING)

    def test_verbosity_setter(self):
        """ Test verbosity setter """
        self.log.verbosity = 'DEBUG'
        self.assertEqual(self.log.verbosity, real_logging.DEBUG)
        self.log.logger.setLevel.assert_called_with(real_logging.DEBUG)

        self.log.verbosity = 'INVALID'
        self.assertEqual(self.log.verbosity, real_logging.ERROR)
        self.log.logger.setLevel.assert_called_with(real_logging.ERROR)


if __name__ == '__main__':
    unittest.main()
