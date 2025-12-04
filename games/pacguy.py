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
import math
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
    # pylint: disable=too-many-instance-attributes, too-many-locals
    # pylint: disable=too-many-branches

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
        self.__ghosts_dir: list[int]
        self.__direction: int
        self.__next_direction: int
        self.__score: int
        self.__alive: bool
        self.__dots: list[tuple[int, int]]
        self.__sound = Sound()
        self.__speed = 0.15
        self.__mouth_open = True
        self.__mouth_animation = Timer(100)
        self.start()

    def start(self) -> None:
        self.__dots = []
        self.__ghosts_pos = []
        self.__ghosts_dir = []
        self.__score = 0
        self.__alive = True
        self.__mouth_open = True
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
                    self.__ghosts_dir.append(random.choice([  # nosec
                        self.__up, self.__down, self.__left, self.__right
                    ]))

        # If no player found, default to top left
        if not hasattr(self, '_PacGuy__player_pos'):
            self.__player_pos = [1.0, 1.0]
        else:
            self.__player_pos = [
                float(self.__player_pos[0]), float(self.__player_pos[1])
            ]

        # Convert ghosts pos to float
        self.__ghosts_pos = [
            [float(g[0]), float(g[1])] for g in self.__ghosts_pos
        ]

        # Ensure ghosts_dir matches ghosts_pos length if re-initializing
        if len(self.__ghosts_dir) != len(self.__ghosts_pos):
            self.__ghosts_dir = [self.__right] * len(self.__ghosts_pos)

    def reset(self) -> None:
        self.start()

    def update(self) -> None:
        if self.__mouth_animation.check():
            self.__mouth_open = not self.__mouth_open

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
        # Current integer position (for grid checks)
        curr_x = int(round(self.__player_pos[0]))
        curr_y = int(round(self.__player_pos[1]))

        # Check if we are close to the center of the tile to allow turning
        dist_x = abs(self.__player_pos[0] - curr_x)
        dist_y = abs(self.__player_pos[1] - curr_y)
        is_centered = dist_x < self.__speed and dist_y < self.__speed

        # Try to change direction
        if self.__next_direction != self.__direction:
            if is_centered and \
               self._can_move([curr_x, curr_y], self.__next_direction):
                self.__direction = self.__next_direction
                # Snap to grid center when turning
                self.__player_pos[0] = float(curr_x)
                self.__player_pos[1] = float(curr_y)

        # Calculate movement
        move_x = 0
        move_y = 0
        if self.__direction == self.__up:
            move_y = -self.__speed
        elif self.__direction == self.__right:
            move_x = self.__speed
        elif self.__direction == self.__down:
            move_y = self.__speed
        elif self.__direction == self.__left:
            move_x = -self.__speed

        # Check collisions ahead
        next_x = self.__player_pos[0] + move_x
        next_y = self.__player_pos[1] + move_y

        # Check collision with wall using a hitbox (radius 0.4)
        hit_wall = False
        radius = 0.4
        if self.__direction == self.__up:
            hit_wall = self._is_wall(next_x - radius, next_y - radius) or \
                self._is_wall(next_x + radius, next_y - radius)
        elif self.__direction == self.__down:
            hit_wall = self._is_wall(next_x - radius, next_y + radius) or \
                self._is_wall(next_x + radius, next_y + radius)
        elif self.__direction == self.__left:
            hit_wall = self._is_wall(next_x - radius, next_y - radius) or \
                self._is_wall(next_x - radius, next_y + radius)
        elif self.__direction == self.__right:
            hit_wall = self._is_wall(next_x + radius, next_y - radius) or \
                self._is_wall(next_x + radius, next_y + radius)

        if hit_wall:
            # Snap to grid if we hit a wall and were moving
            if not is_centered:
                pass
        else:
            self.__player_pos[0] = next_x
            self.__player_pos[1] = next_y

        # Wrap around (tunnel)
        if self.__player_pos[0] < -0.5:
            self.__player_pos[0] = len(self.__map_layout[0]) - 0.5
        elif self.__player_pos[0] >= len(self.__map_layout[0]) - 0.5:
            self.__player_pos[0] = -0.5

    def _move_ghosts(self):
        # pylint: disable=too-many-statements
        for i, ghost in enumerate(self.__ghosts_pos):
            direction = self.__ghosts_dir[i]
            speed = self.__speed * 0.8  # Ghosts are slightly slower

            # Calculate movement
            move_x = 0
            move_y = 0
            if direction == self.__up:
                move_y = -speed
            elif direction == self.__right:
                move_x = speed
            elif direction == self.__down:
                move_y = speed
            elif direction == self.__left:
                move_x = -speed

            # Check collisions ahead
            next_x = ghost[0] + move_x
            next_y = ghost[1] + move_y

            # Determine the tile we are moving into
            check_x = next_x
            check_y = next_y
            if move_x > 0:
                check_x += 0.4
            elif move_x < 0:
                check_x -= 0.4
            if move_y > 0:
                check_y += 0.4
            elif move_y < 0:
                check_y -= 0.4

            # Current integer position
            curr_x = int(round(ghost[0]))
            curr_y = int(round(ghost[1]))

            # Check if centered
            dist_x = abs(ghost[0] - curr_x)
            dist_y = abs(ghost[1] - curr_y)
            is_centered = dist_x < speed and dist_y < speed

            hit_wall = self._is_wall(check_x, check_y)

            if hit_wall:
                # Snap to center and pick new direction
                ghost[0] = float(curr_x)
                ghost[1] = float(curr_y)
                self.__ghosts_dir[i] = self._pick_new_ghost_direction(
                    [curr_x, curr_y], direction
                )
            else:
                ghost[0] = next_x
                ghost[1] = next_y

                # If centered, maybe change direction (randomly)
                if is_centered:
                    # Snap orthogonal axis to ensure we don't drift
                    if direction in [self.__up, self.__down]:
                        ghost[0] = float(curr_x)
                    else:
                        ghost[1] = float(curr_y)

                    # 20% chance to change direction at intersection
                    if random.random() < 0.2:  # nosec
                        new_dir = self._pick_new_ghost_direction(
                            [curr_x, curr_y], direction
                        )
                        if new_dir != direction:
                            # Snap both axes if changing direction
                            ghost[0] = float(curr_x)
                            ghost[1] = float(curr_y)
                            self.__ghosts_dir[i] = new_dir

                # Wrap around (tunnel)
                if ghost[0] < -0.5:
                    ghost[0] = len(self.__map_layout[0]) - 0.5
                elif ghost[0] >= len(self.__map_layout[0]) - 0.5:
                    ghost[0] = -0.5

    def _pick_new_ghost_direction(self, pos, current_dir):
        options = []
        # Prefer not to reverse direction unless necessary
        reverse_dir = (current_dir + 2) % 4

        if self._can_move(pos, self.__up):
            options.append(self.__up)
        if self._can_move(pos, self.__right):
            options.append(self.__right)
        if self._can_move(pos, self.__down):
            options.append(self.__down)
        if self._can_move(pos, self.__left):
            options.append(self.__left)

        # Filter out reverse direction if other options exist
        non_reverse_options = [o for o in options if o != reverse_dir]
        if non_reverse_options:
            return random.choice(non_reverse_options)  # nosec
        if options:
            return random.choice(options)  # nosec
        return current_dir

    def _is_wall(self, x, y):
        # Check if a specific float coordinate is inside a wall
        # We treat the wall as a full 1x1 tile at integer coordinates
        # So if x,y falls into a wall tile, it's a collision
        # However, for smooth movement, we usually check the center or edges
        # of the character against the wall.
        # Here we assume the character is a point or small circle.
        # Let's check the tile containing the point.
        # Since pos is center-based, tile k spans [k-0.5, k+0.5]
        tile_x = int(x + 0.5)
        tile_y = int(y + 0.5)

        # Bounds check
        if tile_x < 0 or tile_x >= len(self.__map_layout[0]):
            return False  # Tunnel
        if tile_y < 0 or tile_y >= len(self.__map_layout):
            return False

        return self.__map_layout[tile_y][tile_x] == '#'

    def _can_move(self, pos, direction):
        # Check if the NEXT tile in the given direction is a wall
        # This is used for decision making (turning)
        x, y = pos
        tile_x = int(round(x))
        tile_y = int(round(y))

        if direction == self.__up:
            tile_y -= 1
        elif direction == self.__right:
            tile_x += 1
        elif direction == self.__down:
            tile_y += 1
        elif direction == self.__left:
            tile_x -= 1

        # Check bounds (allow tunnel entry)
        if tile_x < 0 or tile_x >= len(self.__map_layout[0]):
            return True

        if 0 <= tile_y < len(self.__map_layout):
            return self.__map_layout[tile_y][tile_x] != '#'
        return False

    def _check_collisions(self):
        # Dots
        px, py = self.__player_pos
        # Check if we are close enough to a dot to eat it
        # Simple distance check or grid check
        # Since dots are at integer coordinates:
        grid_x = int(round(px))
        grid_y = int(round(py))

        if (grid_x, grid_y) in self.__dots:
            # Only eat if we are close enough
            if abs(px - grid_x) < 0.4 and abs(py - grid_y) < 0.4:
                self.__dots.remove((grid_x, grid_y))
                self.__score += 10
                self.__sound.tone(600)

        # Ghosts
        for gx, gy in self.__ghosts_pos:
            # Simple distance check
            dist = math.sqrt((px - gx)**2 + (py - gy)**2)
            if dist < 0.8:  # Collision threshold
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
        center_x = (
            self.__player_pos[0] * self.__tile_size + self.__tile_size // 2
        )
        center_y = (
            self.__player_pos[1] * self.__tile_size + self.__tile_size // 2
        )
        center = (center_x, center_y)
        radius = self.__tile_size // 2 - 2

        if not self.__mouth_open:
            pygame.draw.circle(self.screen, (255, 255, 0), center, radius)
            return

        # Angle of the center of the mouth
        if self.__direction == self.__up:
            angle = math.pi / 2
        elif self.__direction == self.__left:
            angle = math.pi
        elif self.__direction == self.__down:
            angle = 3 * math.pi / 2
        else:  # self.__direction == self.__right
            angle = 0

        mouth_angle = math.pi / 4
        start_angle = angle - mouth_angle
        end_angle = angle + mouth_angle

        # Create a list of points for the polygon
        points = [center]
        num_segments = 20  # Smoothness of the arc
        # Iterate from end_angle to start_angle+2pi to draw the body
        for i in range(num_segments + 1):
            theta = end_angle + \
                (start_angle + 2 * math.pi - end_angle) * \
                float(i) / num_segments
            points.append(
                (center[0] + radius * math.cos(theta),
                 center[1] - radius * math.sin(theta))  # Y-axis is inverted
            )
        pygame.draw.polygon(self.screen, (255, 255, 0), points)

    def _draw_ghosts(self):
        colors = [(255, 0, 0), (255, 184, 255),
                  (0, 255, 255), (255, 184, 82)]
        for i, (x, y) in enumerate(self.__ghosts_pos):
            body_color = colors[i % len(colors)]
            eye_color = (255, 255, 255)
            pupil_color = (0, 0, 0)
            x_pixel = x * self.__tile_size + 2
            y_pixel = y * self.__tile_size + 2
            width = self.__tile_size - 4
            height = self.__tile_size - 4
            # Ghost body
            pygame.draw.arc(
                self.screen, body_color,
                (x_pixel, y_pixel, width, height),
                0, math.pi, width // 2
            )
            pygame.draw.rect(
                self.screen, body_color,
                (x_pixel, y_pixel + height // 2, width, height // 2)
            )
            # Ghost eyes
            eye_y = y_pixel + height // 4
            pupil_y = eye_y + 2
            for i in range(2):
                eye_x = x_pixel + (i * width // 2) + width // 4
                pupil_x = eye_x
                pygame.draw.circle(
                    self.screen, eye_color,
                    (eye_x, eye_y), width // 6
                )
                pygame.draw.circle(
                    self.screen, pupil_color,
                    (pupil_x, pupil_y), width // 12
                )

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
