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
# pylint: disable=no-name-in-module
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_r, K_u, K_BACKSPACE
)

from src.game_template import Game
from src.font import Font


class M2048(Game):  # pylint: disable=too-many-instance-attributes
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
        self.history = []

        # Animation state
        self.animations = []
        self.animating = False
        self.undoing = False
        self.game_over_active = False
        self.animation_start_time = 0
        self.animation_duration = 150  # ms

        self.reset()

    def start(self) -> None:
        """ Start game match """
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.animations = []
        self.animating = False
        self.undoing = False
        self.game_over_active = False
        self._spawn_tile()
        self._spawn_tile()

    def reset(self) -> None:
        """ Restart game match """
        self.start()

    def game_over(self) -> None:
        """ Game over """
        self.game_over_active = True
        print("Game Over!")

    def update(self) -> None:
        """ Update game match """
        self.canvas.fill((187, 173, 160))  # Background color

        current_time = pygame.time.get_ticks()

        if self.animating:
            progress = (
                (current_time - self.animation_start_time) /
                self.animation_duration
            )
            if progress >= 1.0:
                progress = 1.0
                self.animating = False
                self.animations = []
                if not self.undoing:
                    self._spawn_tile()  # Spawn tile after animation
                    if self._check_game_over():
                        self.game_over()
                self.undoing = False

            # Draw static background grid
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    self._draw_tile_bg(r, c)

            # Draw animating tiles
            for anim in self.animations:
                value = anim['value']
                if value == 0:
                    continue

                start_r, start_c = anim['from']
                end_r, end_c = anim['to']

                # Interpolate position
                curr_r = start_r + (end_r - start_r) * progress
                curr_c = start_c + (end_c - start_c) * progress

                self._draw_tile_at(curr_r, curr_c, value)

        else:
            # Draw static grid
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    self._draw_tile_bg(r, c)
                    value = self.grid[r][c]
                    if value != 0:
                        self._draw_tile_at(r, c, value)

        self.screen.blit(self.canvas, (0, 0))

        if self.game_over_active:
            # Draw overlay
            overlay = pygame.Surface(
                (self.canvas.get_width(), self.canvas.get_height()),
                pygame.SRCALPHA
            )
            overlay.fill((238, 228, 218, 180))  # Semi-transparent background
            self.screen.blit(overlay, (0, 0))

            # Draw Game Over text
            font_large = pygame.font.SysFont('Arial', 60, bold=True)
            text_surface = font_large.render("Game Over!", True, (119, 110, 101))
            text_rect = text_surface.get_rect(
                center=(self.canvas.get_width() / 2, self.canvas.get_height() / 2 - 50)
            )
            self.screen.blit(text_surface, text_rect)

            # Draw instructions
            font_small = pygame.font.SysFont('Arial', 30)
            instr_surface = font_small.render(
                "Press R to Restart or U to Undo", True, (119, 110, 101)
            )
            instr_rect = instr_surface.get_rect(
                center=(self.canvas.get_width() / 2, self.canvas.get_height() / 2 + 20)
            )
            self.screen.blit(instr_surface, instr_rect)

    def _draw_tile_bg(self, r, c):
        rect = pygame.Rect(
            c * (self.tile_size + self.tile_margin) + self.tile_margin,
            r * (self.tile_size + self.tile_margin) + self.tile_margin,
            self.tile_size,
            self.tile_size
        )
        # Empty cell color
        pygame.draw.rect(self.canvas, (205, 193, 180), rect)

    def _draw_tile_at(self, r, c, value):
        color = self.__colors.get(value, (60, 58, 50))
        x = c * (self.tile_size + self.tile_margin) + self.tile_margin
        y = r * (self.tile_size + self.tile_margin) + self.tile_margin

        rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        pygame.draw.rect(self.canvas, color, rect)

        if value != 0:
            font = pygame.font.SysFont('Arial', 40, bold=True)
            text_color = (119, 110, 101) if value <= 4 else (249, 246, 242)
            text_surface = font.render(str(value), True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.canvas.blit(text_surface, text_rect)

    def save_state(self, moves):
        """ Save current game state """
        self.history.append({
            'grid': [row[:] for row in self.grid],
            'score': self.score,
            'moves': moves
        })

    def undo(self):
        """ Undo last move """
        if not self.history:
            return

        state = self.history.pop()
        self.grid = state['grid']
        self.score = state['score']

        # Reverse animations
        reverse_moves = []
        for move in state['moves']:
            reverse_moves.append({
                'value': move['value'],
                'from': move['to'],
                'to': move['from']
            })

        self.animations = reverse_moves
        self.animating = True
        self.undoing = True
        self.game_over_active = False
        self.animation_start_time = pygame.time.get_ticks()

    def control(self, keys, joystick) -> None:
        """ Receive control commands """
        if K_ESCAPE in keys:
            self.stop()
        if K_r in keys:
            self.reset()
        if K_u in keys or K_BACKSPACE in keys:
            self.undo()

        if self.animating:
            return

        if self.game_over_active:
            return

        # Save state before attempting move
        current_grid = [row[:] for row in self.grid]
        current_score = self.score

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
            # If move was successful, push the PREVIOUS state to history
            # We need to capture the moves that transitioned FROM current_grid TO self.grid
            # self.animations currently holds these moves.
            self.save_state(self.animations)

            self.animating = True
            self.animation_start_time = pygame.time.get_ticks()
            # Spawn tile is now handled in update() after animation finishes

    def _spawn_tile(self):
        empty_cells = [
            (r, c) for r in range(self.grid_size)
            for c in range(self.grid_size) if self.grid[r][c] == 0
        ]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def _move(self, direction):
        if direction in ('UP', 'DOWN'):
            return self._move_vertical(direction)
        if direction in ('LEFT', 'RIGHT'):
            return self._move_horizontal(direction)
        return False

    def _move_vertical(self, direction):
        moves = []
        grid_changed = False
        is_down = direction == 'DOWN'

        for c in range(self.grid_size):
            col = [self.grid[r][c] for r in range(self.grid_size)]
            if is_down:
                col = col[::-1]

            new_col, col_moves = self._merge(col)
            if is_down:
                new_col = new_col[::-1]

            if new_col != [self.grid[r][c] for r in range(self.grid_size)]:
                grid_changed = True

            for r in range(self.grid_size):
                self.grid[r][c] = new_col[r]

            for m in col_moves:
                if is_down:
                    orig_from = self.grid_size - 1 - m['from']
                    orig_to = self.grid_size - 1 - m['to']
                    moves.append({
                        'value': m['value'],
                        'from': (orig_from, c),
                        'to': (orig_to, c)
                    })
                else:
                    moves.append({
                        'value': m['value'],
                        'from': (m['from'], c),
                        'to': (m['to'], c)
                    })

        if grid_changed:
            self.animations = moves
            return True
        return False

    def _move_horizontal(self, direction):
        moves = []
        grid_changed = False
        is_right = direction == 'RIGHT'

        for r in range(self.grid_size):
            row = self.grid[r]
            if is_right:
                row = row[::-1]

            new_row, row_moves = self._merge(row)
            if is_right:
                new_row = new_row[::-1]

            if new_row != self.grid[r]:
                grid_changed = True
            self.grid[r] = new_row

            for m in row_moves:
                if is_right:
                    orig_from = self.grid_size - 1 - m['from']
                    orig_to = self.grid_size - 1 - m['to']
                    moves.append({
                        'value': m['value'],
                        'from': (r, orig_from),
                        'to': (r, orig_to)
                    })
                else:
                    moves.append({
                        'value': m['value'],
                        'from': (r, m['from']),
                        'to': (r, m['to'])
                    })

        if grid_changed:
            self.animations = moves
            return True
        return False

    def _merge(self, line):
        non_zero = []
        for i, val in enumerate(line):
            if val != 0:
                non_zero.append({'val': val, 'orig_index': i})

        merged_line = []
        moves = []
        skip = False

        target_index = 0
        for i, current in enumerate(non_zero):
            if skip:
                skip = False
                continue

            if (i + 1 < len(non_zero) and
                    current['val'] == non_zero[i + 1]['val']):
                # Merge
                next_tile = non_zero[i + 1]
                new_val = current['val'] * 2
                self.score += new_val

                moves.append({
                    'from': current['orig_index'],
                    'to': target_index,
                    'value': current['val'],
                    'merged': False
                })
                moves.append({
                    'from': next_tile['orig_index'],
                    'to': target_index,
                    'value': next_tile['val'],
                    'merged': True
                })

                merged_line.append(new_val)
                skip = True
            else:
                # No merge
                moves.append({
                    'from': current['orig_index'],
                    'to': target_index,
                    'value': current['val'],
                    'merged': False
                })
                merged_line.append(current['val'])

            target_index += 1

        # Pad with zeros
        final_line = merged_line + [0] * (len(line) - len(merged_line))

        return final_line, moves

    def _check_game_over(self):
        # Check for empty cells
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == 0:
                    return False

        # Check for possible merges
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (c + 1 < self.grid_size and
                        self.grid[r][c] == self.grid[r][c + 1]):
                    return False
                if (r + 1 < self.grid_size and
                        self.grid[r][c] == self.grid[r + 1][c]):
                    return False

        return True
