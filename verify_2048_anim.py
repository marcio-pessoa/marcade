
import pygame
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from games.m2048 import M2048
from pygame.locals import K_RIGHT

def test_animation_logic():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game = M2048(screen)
    game.start()

    print("Initial State:")
    print(f"Tiles: {len(game.tiles)}")
    print(f"Animating: {game.animating}")

    # Force a specific state for testing
    # Clear grid
    game.tiles = []
    game.grid = [[None]*4 for _ in range(4)]

    # Add two tiles that can merge
    from games.m2048 import Tile
    t1 = Tile(2, 0, 0, 10, 10) # Top-left
    t2 = Tile(2, 0, 1, 120, 10) # Top-left + 1
    game.tiles.extend([t1, t2])
    game.grid[0][0] = t1
    game.grid[0][1] = t2

    # Update target coords based on grid (just to be safe)
    t1.target_x, t1.target_y = game._get_coords(0, 0)
    t2.target_x, t2.target_y = game._get_coords(0, 1)
    t1.x, t1.y = t1.target_x, t1.target_y
    t2.x, t2.y = t2.target_x, t2.target_y

    print(f"Before Move: T1 at ({t1.row}, {t1.col}), T2 at ({t2.row}, {t2.col})")

    # Simulate Right Key Press
    print("Pressing RIGHT...")
    game.control([K_RIGHT], None)

    print(f"Animating: {game.animating}")
    if not game.animating:
        print("FAIL: Should be animating")
        return

    # Check targets
    # T2 is at (0, 1). T1 is at (0, 0).
    # Moving RIGHT:
    # T2 should move to (0, 3).
    # T1 should move to (0, 2).
    # Wait, they are both 2. They should merge?
    # Row: [2, 2, 0, 0] -> Move Right -> [0, 0, 0, 4]
    # So T2 moves to (0, 3). T1 moves to (0, 3) and merges.

    print("Checking targets...")
    for t in game.tiles:
        if t.visible: # Only check visible ones (original tiles)
            print(f"Tile val={t.value} target=({t.target_x}, {t.target_y})")

    # Simulate frames
    print("Simulating frames...")
    for i in range(20):
        game.update()
        if not game.animating:
            print(f"Animation finished at frame {i}")
            break

    print(f"Final Tiles: {len(game.tiles)}")
    for t in game.tiles:
        print(f"Tile val={t.value} pos=({t.row}, {t.col})")

    # Should have 1 tile of value 4 (plus one random spawn)
    val4 = [t for t in game.tiles if t.value == 4]
    if len(val4) >= 1:
        print("SUCCESS: Merge happened")
    else:
        print("FAIL: No merged tile found")

if __name__ == "__main__":
    test_animation_logic()
