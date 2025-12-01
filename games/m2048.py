"""
---
name: m2048.py
description: 2048 Game Module
contributors:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import random
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_r

from src.game_template import Game
from src.font import Font


class M2048(Game):
    """ 2048 Game class """

    __version__ = '0.1.0'
    __colors = {
        0: (205, 193, 180),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
    }

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.grid_size = 4
        self.tile_size = 100
        self.tile_margin = 10
        self.score = 0
        self.grid = []
        self.font = Font(self.canvas)
        self.font.size = 5
        self.reset()

    def start(self) -> None:
        """ Start game match """
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self._spawn_tile()
        self._spawn_tile()

    def reset(self) -> None:
        """ Restart game match """
        self.start()

    def game_over(self) -> None:
        """ Game over """
        # Simple game over indication for now, could be improved
        print("Game Over!")

    def update(self) -> None:
        """ Update game match """
        self.canvas.fill((187, 173, 160))  # Background color

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                value = self.grid[r][c]
                color = self.__colors.get(value, (60, 58, 50))
                rect = pygame.Rect(
                    c * (self.tile_size + self.tile_margin) + self.tile_margin,
                    r * (self.tile_size + self.tile_margin) + self.tile_margin,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(self.canvas, color, rect)

                if value != 0:
                    # Draw text manually or use a font helper if available.
                    # Since src.font.Font seems to be a custom sprite font,
                    # let's try to use it or fallback to basic pygame font if needed.
                    # The existing Font class seems to draw text at a position.
                    # For now, let's use a simple system font for numbers as the custom Font
                    # might not support all numbers or scaling easily without more investigation.
                    # Actually, looking at invasion.py, Font is used for score.
                    # Let's stick to Pygame's default font for simplicity and readability of numbers.
                    font = pygame.font.SysFont('Arial', 40, bold=True)
                    text_color = (119, 110, 101) if value <= 4 else (249, 246, 242)
                    text_surface = font.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.canvas.blit(text_surface, text_rect)

        self.screen.blit(self.canvas, (0, 0))

    def control(self, keys, joystick) -> None:
        """ Receive control commands """
        if K_ESCAPE in keys:
            self.stop()
        if K_r in keys:
            self.reset()

        moved = False
        if K_UP in keys:
            moved = self._move('UP')
        elif K_DOWN in keys:
            moved = self._move('DOWN')
        elif K_LEFT in keys:
            moved = self._move('LEFT')
        elif K_RIGHT in keys:
            moved = self._move('RIGHT')

        if moved:
            self._spawn_tile()
            if self._check_game_over():
                self.game_over()

    def _spawn_tile(self):
        empty_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def _move(self, direction):
        moved = False
        if direction == 'UP':
            for c in range(self.grid_size):
                col = [self.grid[r][c] for r in range(self.grid_size)]
                new_col, col_moved = self._merge(col)
                if col_moved:
                    moved = True
                for r in range(self.grid_size):
                    self.grid[r][c] = new_col[r]
        elif direction == 'DOWN':
            for c in range(self.grid_size):
                col = [self.grid[r][c] for r in range(self.grid_size)]
                new_col, col_moved = self._merge(col[::-1])
                if col_moved:
                    moved = True
                for r in range(self.grid_size):
                    self.grid[r][c] = new_col[::-1][r]
        elif direction == 'LEFT':
            for r in range(self.grid_size):
                row = self.grid[r]
                new_row, row_moved = self._merge(row)
                if row_moved:
                    moved = True
                self.grid[r] = new_row
        elif direction == 'RIGHT':
            for r in range(self.grid_size):
                row = self.grid[r]
                new_row, row_moved = self._merge(row[::-1])
                if row_moved:
                    moved = True
                self.grid[r] = new_row[::-1]
        return moved

    def _merge(self, line):
        non_zero = [x for x in line if x != 0]
        merged = []
        skip = False
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged.append(non_zero[i] * 2)
                self.score += non_zero[i] * 2
                skip = True
            else:
                merged.append(non_zero[i])

        # Pad with zeros
        new_line = merged + [0] * (len(line) - len(merged))
        return new_line, new_line != line

    def _check_game_over(self):
        # Check for empty cells
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == 0:
                    return False

        # Check for possible merges
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if c + 1 < self.grid_size and self.grid[r][c] == self.grid[r][c+1]:
                    return False
                if r + 1 < self.grid_size and self.grid[r][c] == self.grid[r+1][c]:
                    return False

        return True
