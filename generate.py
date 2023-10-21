import random
from enum import Enum
import numpy as np
import cv2
import sys
from constants import CELL_SIZE, RECURSION_LIMIT

sys.setrecursionlimit(RECURSION_LIMIT)


class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class MazeGenerator:
    """Maze generator class"""

    def __init__(self, height: int, width: int):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.maze = np.ones((self.height, self.width), dtype=np.float16)
        self.big_maze = np.zeros(
            ((self.height - 2) * CELL_SIZE, (self.width - 2) * CELL_SIZE),
            dtype=np.float16,
        )

        self._generate()

    def _generate(self):
        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    self.maze[i, j] = 0
                if i == 0 or j == 0 or i == self.height - 1 or j == self.width - 1:
                    self.maze[i, j] = 0.5

        sx = random.choice(range(2, self.width - 2, 2))
        sy = random.choice(range(2, self.height - 2, 2))

        self._backtrack(sx, sy, self.maze)

        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i, j] == 0.5:
                    self.maze[i, j] = 1

        self.maze[1, 2] = 1
        self.maze[self.height - 2, self.width - 3] = 1
        self.maze = self.maze[1 : self.height - 1, 1 : self.width - 1]

        for i in range(self.height - 2):
            for j in range(self.width - 2):
                if self.maze[i, j] == 1:
                    self.big_maze[
                        i * CELL_SIZE : (i + 1) * CELL_SIZE,
                        j * CELL_SIZE : (j + 1) * CELL_SIZE,
                    ] = 1

        self.maze = self.maze * 255.0
        self.big_maze = self.big_maze * 255.0

        return

    def _backtrack(self, cx, cy, grid):
        grid[cy, cx] = 0.5

        if (
            grid[cy - 2, cx] == 0.5
            and grid[cy + 2, cx] == 0.5
            and grid[cy, cx - 2] == 0.5
            and grid[cy, cx + 2] == 0.5
        ):
            return

        li = [1, 2, 3, 4]
        while len(li) > 0:
            dir = random.choice(li)
            li.remove(dir)

            if dir == Directions.UP.value:
                ny = cy - 2
                my = cy - 1
            elif dir == Directions.DOWN.value:
                ny = cy + 2
                my = cy + 1
            else:
                ny = cy
                my = cy

            if dir == Directions.LEFT.value:
                nx = cx - 2
                mx = cx - 1
            elif dir == Directions.RIGHT.value:
                nx = cx + 2
                mx = cx + 1
            else:
                nx = cx
                mx = cx

            if grid[ny, nx] != 0.5:
                grid[my, mx] = 0.5
                self._backtrack(nx, ny, grid)

    def save_image(self, path: str):
        cv2.imwrite(path, self.big_maze)

    def get_maze(self):
        return np.uint8(self.big_maze)
