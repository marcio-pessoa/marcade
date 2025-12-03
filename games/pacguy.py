"""
---
name: pacguy.py
description: Pac-Guy game package file
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import sys
import random
import pygame
try:
    from pygame.locals import K_ESCAPE, K_UP, K_RIGHT, K_DOWN, K_LEFT
except ImportError as err:
    print("Could not load module. " + str(err))
    sys.exit(True)

from src.font import Font
from src.game_template import Game
from src.sound import Sound
from src.timer import Timer


class PacGuy(Game):
    """ PacGuy game class """

    __version__ = '0.1.0'
    __up = 0
    __right = 1
    __down = 2
    __left = 3
    __tile_size = 20

    # Map definition
    # #: Wall
    # .: Dot
    #  : Empty
    # P: Player
    # G: Ghost
    __map_layout = [
        "############################",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#..........................#",
        "#.####.##.########.##.####.#",
        "#......##....##....##......#",
        "######.##### ## #####.######",
        "     #.##          ##.#     ",
        "     #.## ###--### ##.#     ",
        "######.## # G  G # ##.######",
        "      .   # G  G #   .      ",
        "######.## #      # ##.######",
        "     #.## ######## ##.#     ",
        "     #.##          ##.#     ",
        "     #.## ######## ##.#     ",
        "######.## ######## ##.######",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#...##................##...#",
        "###.##.##.########.##.##.###",
        "#......##....##....##......#",
        "#.##########.##.##########.#",
        "#..........................#",
        "############################",
    ]

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.__player_pos: list[int]
        self.__ghosts_pos: list[list[int]]
        self.__direction: int
        self.__next_direction: int
        self.__score: int
        self.__alive: bool
        self.__dots: list[tuple[int, int]]
        self.__sound = Sound()
        self.__update = Timer(150)  # Speed of the game
        self.start()

    def start(self) -> None:
        self.__dots = []
        self.__ghosts_pos = []
        self.__score = 0
        self.__alive = True
        self.__direction = self.__right
        self.__next_direction = self.__right

        # Parse map
        for y, row in enumerate(self.__map_layout):
            for x, char in enumerate(row):
                if char == '.':
                    self.__dots.append((x, y))
                elif char == 'P':
                    self.__player_pos = [x, y]
                elif char == 'G':
                    self.__ghosts_pos.append([x, y])

        # If no player found, default to top left
        if not hasattr(self, '_PacGuy__player_pos'):
            self.__player_pos = [1, 1]

    def reset(self) -> None:
        self.start()

    def update(self) -> None:
        if not self.__update.check():
            return

        if self.__alive:
            self._move_player()
            self._move_ghosts()
            self._check_collisions()

        self.screen.fill((0, 0, 0))
        self._draw_map()
        self._draw_dots()
        self._draw_player()
        self._draw_ghosts()
        self._draw_score()

        if not self.__alive:
            self.game_over()

    def control(self, keys, joystick) -> None:
        if K_ESCAPE in keys:
            self.stop()

        new_dir = -1
        if K_UP in keys:
            new_dir = self.__up
        elif K_RIGHT in keys:
            new_dir = self.__right
        elif K_DOWN in keys:
            new_dir = self.__down
        elif K_LEFT in keys:
            new_dir = self.__left

        if new_dir != -1:
            self.__next_direction = new_dir

    def _move_player(self):
        # Try to change direction if possible
        if self._can_move(self.__player_pos, self.__next_direction):
            self.__direction = self.__next_direction

        if self._can_move(self.__player_pos, self.__direction):
            if self.__direction == self.__up:
                self.__player_pos[1] -= 1
            elif self.__direction == self.__right:
                self.__player_pos[0] += 1
            elif self.__direction == self.__down:
                self.__player_pos[1] += 1
            elif self.__direction == self.__left:
                self.__player_pos[0] -= 1

        # Wrap around (tunnel)
        if self.__player_pos[0] < 0:
            self.__player_pos[0] = len(self.__map_layout[0]) - 1
        elif self.__player_pos[0] >= len(self.__map_layout[0]):
            self.__player_pos[0] = 0

    def _move_ghosts(self):
        for ghost in self.__ghosts_pos:
            # Simple random movement for now
            options = []
            if self._can_move(ghost, self.__up):
                options.append(self.__up)
            if self._can_move(ghost, self.__right):
                options.append(self.__right)
            if self._can_move(ghost, self.__down):
                options.append(self.__down)
            if self._can_move(ghost, self.__left):
                options.append(self.__left)

            if options:
                move = random.choice(options)  # nosec
                if move == self.__up:
                    ghost[1] -= 1
                elif move == self.__right:
                    ghost[0] += 1
                elif move == self.__down:
                    ghost[1] += 1
                elif move == self.__left:
                    ghost[0] -= 1

    def _can_move(self, pos, direction):
        x, y = pos
        if direction == self.__up:
            y -= 1
        elif direction == self.__right:
            x += 1
        elif direction == self.__down:
            y += 1
        elif direction == self.__left:
            x -= 1

        # Check bounds (allow tunnel entry)
        if x < 0 or x >= len(self.__map_layout[0]):
            return True

        if 0 <= y < len(self.__map_layout):
            return self.__map_layout[y][x] != '#'
        return False

    def _check_collisions(self):
        # Dots
        px, py = self.__player_pos
        if (px, py) in self.__dots:
            self.__dots.remove((px, py))
            self.__score += 10
            self.__sound.tone(600)

        # Ghosts
        for gx, gy in self.__ghosts_pos:
            if px == gx and py == gy:
                self.__alive = False
                self.__sound.tone(200)

    def _draw_map(self):
        for y, row in enumerate(self.__map_layout):
            for x, char in enumerate(row):
                if char == '#':
                    rect = (x * self.__tile_size,
                            y * self.__tile_size,
                            self.__tile_size,
                            self.__tile_size)
                    pygame.draw.rect(self.screen, (0, 0, 150), rect, 1)

    def _draw_dots(self):
        for x, y in self.__dots:
            center = (x * self.__tile_size + self.__tile_size // 2,
                      y * self.__tile_size + self.__tile_size // 2)
            pygame.draw.circle(self.screen, (255, 184, 174), center, 3)

    def _draw_player(self):
        center = (self.__player_pos[0] * self.__tile_size +
                  self.__tile_size // 2,
                  self.__player_pos[1] * self.__tile_size +
                  self.__tile_size // 2)
        radius = self.__tile_size // 2 - 2
        pygame.draw.circle(self.screen, (255, 255, 0), center, radius)

    def _draw_ghosts(self):
        colors = [(255, 0, 0), (255, 184, 255),
                  (0, 255, 255), (255, 184, 82)]
        for i, (x, y) in enumerate(self.__ghosts_pos):
            rect = (x * self.__tile_size + 2, y * self.__tile_size + 2,
                    self.__tile_size - 4, self.__tile_size - 4)
            pygame.draw.rect(self.screen, colors[i % len(colors)], rect)

    def _draw_score(self):
        # Simple score display
        pass

    def game_over(self):
        message = Font(self.screen)
        message.size = 9
        message.position = [161, 120]
        message.color = (255, 255, 255)
        message.echo("GAME OVER")
        score = Font(self.screen)
        score.size = 9
        score.position = [186, 300]
        score.color = (255, 255, 255)
        score.echo(f'SCORE {self.__score}')
        return super().game_over()
