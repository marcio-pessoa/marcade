
import sys
import os
import pygame

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

try:
    from games.m2048 import M2048

    # Initialize pygame headless
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((800, 600))
    game = M2048(screen)

    print("Game initialized successfully")

    game.start()
    print("Game started successfully")

    game.update()
    print("Game updated successfully")

    # Test a move
    game._move('UP')
    print("Game move logic executed successfully")

except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)

print("SUCCESS")
