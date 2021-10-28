#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
name: joystick_test.py
description: Test Joystick package
copyright: 2019-2019 Marcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
change-log:
  2019-09-01
  - version: 0.2
    fixed: improved tests
  2019-08-31
  - version: 0.1
    added: timer tests
"""

import sys
import pygame
from joystick import Joystick, detect

# Detect and initialize joystick
JOYSTICK = Joystick()
if detect():
    JOYSTICK.identification(detect()[0])
else:
    print("Joystick not found.")
    sys.exit(True)

# Display joystick configuration
print("Joystick configuration:")
print(JOYSTICK.configuration())

pygame.init()  # pylint: disable=no-member

# Used to manage how fast the screen updates.
CLOCK = pygame.time.Clock()

while True:
    # Check user actions
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:  # pylint: disable=no-member
            print(JOYSTICK.axis())
        elif event.type == pygame.JOYBALLMOTION:  # pylint: disable=no-member
            print(JOYSTICK.ball())
        elif event.type == pygame.JOYBUTTONDOWN:  # pylint: disable=no-member
            print(JOYSTICK.button())
        elif event.type == pygame.JOYBUTTONUP:  # pylint: disable=no-member
            print(JOYSTICK.button())
        elif event.type == pygame.JOYHATMOTION:  # pylint: disable=no-member
            print(JOYSTICK.hat())
    # Limit to 10 frames per second.
    CLOCK.tick(10)

pygame.quit()  # pylint: disable=no-member
