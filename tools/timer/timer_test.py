#!/usr/bin/env python3
"""
---
name: timer_test.py
description: Test Timer package
copyright: 2019-2019 Marcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
change-log:
  2019-08-26
  - version: 0.1
    added: timer tests
"""

import time
import unittest
from timer import Timer


class TestTimerMethods(unittest.TestCase):
    """
    description:
    """

    def test_get_period(self):
        """
        description: get() method must return defined time period.
        """
        period = 1000
        timer = Timer(period)
        self.assertEqual(timer.get(), period)

    def test_status(self):
        """
        description: status() method must return current time, so it is a number
                     between 0 and defined period.
        """
        period = 10
        timer = Timer(period)
        self.assertLessEqual(timer.status(), period)

    def test_set(self):
        """
        description: set() method must configure a new time period.
        """
        period = 10
        timer = Timer(period)
        period = 20
        timer.set(period)
        self.assertEqual(timer.get(), period)

    def test_reset(self):
        """
        description: reset() is used to reset (obviously) a timer counter.
        """
        period = 100
        timer = Timer(period)
        time.sleep((period - 10) / 1000)
        timer.reset()
        self.assertLessEqual(timer.status(), 1)

    def test_countdown(self):
        """
        description:
        """
        period = 100
        timer = Timer(period, 'COUNTDOWN')
        time.sleep(period / 1000)
        self.assertGreaterEqual(timer.status(), period)

    def test_loop(self):
        """
        description: Test a loop timer
        """
        period = 10
        timer = Timer(period)
        time.sleep(period / 2 / 1000)
        self.assertEqual(timer.check(), False)
        time.sleep(period / 2 / 1000)
        self.assertEqual(timer.check(), True)

    def test_stopwatch(self):
        """
        description:
        """
        period = 100
        timer = Timer(period, 'STOPWATCH')
        time.sleep(period / 1000)
        self.assertGreaterEqual(timer.check(), period)

    def test_disable(self):
        """
        description: disable() is used to timer always return False
        """
        period = 100
        timer = Timer(period)
        timer.disable()
        time.sleep(period / 1000)
        self.assertEqual(timer.check(), False)

    def test_enable(self):
        """
        description: enable() is used to turn on a timer
        """
        period = 100
        timer = Timer(period)
        timer.disable()
        timer.enable()
        time.sleep(period / 1000)
        self.assertEqual(timer.check(), True)


if __name__ == '__main__':
    unittest.main()
