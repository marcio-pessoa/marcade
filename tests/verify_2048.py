"""
Verify 2048 Game Logic Script
"""

import sys
import os
import pygame  # pylint: disable=no-member

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

try:
    from games.m2048 import M2048

    # Initialize pygame headless
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()  # pylint: disable=no-member
    pygame.font.init()

    screen = pygame.display.set_mode((800, 600))
    game = M2048(screen)

    print("Game initialized successfully")

    game.start()
    print("Game started successfully")

    game.update()
    print("Game updated successfully")

    # Test a move
    game._move('UP')  # pylint: disable=protected-access
    print("Game move logic executed successfully")

except Exception as e:  # pylint: disable=broad-exception-caught
    print(f"FAILED: {e}")
    sys.exit(1)

print("SUCCESS")
