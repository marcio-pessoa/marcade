#!/usr/bin/env python3
"""
---
name: timer_test.py
description: Test Timer package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import unittest
from unittest.mock import patch
from src.timer import Timer


class TestTimerMethods(unittest.TestCase):
    """
    description:
    """

    @patch('src.timer.time.time')
    def test_get_period(self, mock_time):
        """
        description: get() method must return defined time period.
        """
        mock_time.return_value = 0
        period = 1000
        timer = Timer(period)
        self.assertEqual(timer.period, period)

    @patch('src.timer.time.time')
    def test_status(self, mock_time):
        """
        status() method must return current time, so it is a number between 0
        and defined period.
        """
        mock_time.return_value = 0
        period = 10
        timer = Timer(period)
        mock_time.return_value = 0.005  # 5ms
        self.assertLessEqual(timer.status(), period)

    @patch('src.timer.time.time')
    def test_set(self, mock_time):
        """
        description: set() method must configure a new time period.
        """
        mock_time.return_value = 0
        period = 10
        timer = Timer(period)
        period = 20
        timer.period = period
        self.assertEqual(timer.period, period)

    @patch('src.timer.time.time')
    def test_reset(self, mock_time):
        """
        description: reset() is used to reset (obviously) a timer counter.
        """
        mock_time.return_value = 0
        period = 100
        timer = Timer(period)
        mock_time.return_value = 0.090  # 90ms
        timer.reset()
        mock_time.return_value = 0.090  # Still 90ms
        self.assertLessEqual(timer.status(), 1)

    @patch('src.timer.time.time')
    def test_countdown(self, mock_time):
        """
        description:
        """
        mock_time.return_value = 0
        period = 100
        timer = Timer(period, 'COUNTDOWN')
        mock_time.return_value = 0.100  # 100ms
        self.assertGreaterEqual(timer.status(), period)

    @patch('src.timer.time.time')
    def test_loop(self, mock_time):
        """
        description: Test a loop timer
        """
        mock_time.return_value = 0
        period = 10
        timer = Timer(period)

        mock_time.return_value = 0.005  # 5ms
        self.assertEqual(timer.check(), False)

        mock_time.return_value = 0.010  # 10ms
        self.assertEqual(timer.check(), True)

    @patch('src.timer.time.time')
    def test_stopwatch(self, mock_time):
        """
        description:
        """
        mock_time.return_value = 0
        period = 100
        timer = Timer(period, 'STOPWATCH')
        mock_time.return_value = 0.100  # 100ms
        self.assertGreaterEqual(timer.check(), period)

    @patch('src.timer.time.time')
    def test_disable(self, mock_time):
        """
        description: disable() is used to timer always return False
        """
        mock_time.return_value = 0
        period = 100
        timer = Timer(period)
        timer.disable()
        mock_time.return_value = 0.100  # 100ms
        self.assertEqual(timer.check(), False)

    @patch('src.timer.time.time')
    def test_enable(self, mock_time):
        """
        description: enable() is used to turn on a timer
        """
        mock_time.return_value = 0
        period = 100
        timer = Timer(period)
        timer.disable()
        timer.enable()
        mock_time.return_value = 0.100  # 100ms
        self.assertEqual(timer.check(), True)
