import pygame
from constants import SCREEN_RESOLUTION, COLORS

Iblock = [
    [1,], 
    [1,], 
    [1,], 
    [1,]
]
Tblock = [
    [0, 2, 0,], 
    [2, 2, 2,],
]

class World:
    """Class that defines the world in which the agents will live.
    The world size is of 300x600 by default and contains 20 rows by 10 columns with a cell size of 30.
    """

    def __init__(self) -> None:
        self.rows = 20
        self.columns = 10
        self.cell_size = 30
        self.size = (self.columns * self.cell_size, self.rows * self.cell_size)

        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

        self.block = Tblock
        self.block_offset = [int(self.columns/2)-1, 0]

    def rotate(self):
        self.block = list(zip(*self.block[::-1]))
        if self.block_offset[0] >= self.columns - len(self.block[0]) + 1:
            self.block_offset[0] = self.columns - len(self.block[0])

    def detect_collision(self):
        # Detect end of screen
        if self.block_offset[0] < 0:
            return True
        if self.block_offset[0] >= self.columns - len(self.block[0]) + 1:
            return True
        # Vertical collision
        if self.block_offset[1] > self.rows - len(self.block):
            return True
        # detect if there are blocks on the sides
        for i, block_row in enumerate(self.block):
            for j, block_element in enumerate(block_row):
                if block_element != 0:
                    if self.grid[i + self.block_offset[1]][j + self.block_offset[0]] != 0:
                        return True
        
        
    def move(self, x, y):
        self.block_offset[0] += x
        if self.detect_collision():
            self.block_offset[0] -= x

        self.block_offset[1] += y
        if self.detect_collision():
            self.block_offset[1] -= y
            self.fix_block()
            self.block_offset = [0, 0]

    def fix_block(self):
        for i, block_row in enumerate(self.block):
            for j, block_element in enumerate(block_row):
                if block_element != 0:
                    self.grid[i + self.block_offset[1]][j + self.block_offset[0]] = block_element

    def draw(self, screen) -> None:
        """draws the world in the middle of the screen"""
        for i in range(self.rows):
            for j in range(self.columns):
                pos = (
                    j * self.cell_size + SCREEN_RESOLUTION[0] / 2 - self.size[0] / 2,
                    i * self.cell_size + SCREEN_RESOLUTION[1] / 2 - self.size[1] / 2,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(
                    screen,
                    COLORS[self.grid[i][j]],
                    pos,
                    1 if self.grid[i][j] == 0 else 0,
                )

        for i, block_row in enumerate(self.block):
            for j, block_element in enumerate(block_row):
                pos = (
                    j * self.cell_size + SCREEN_RESOLUTION[0] / 2 - self.size[0] / 2 + self.block_offset[0] * self.cell_size,
                    i * self.cell_size + SCREEN_RESOLUTION[1] / 2 - self.size[1] / 2 + self.block_offset[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                if block_element != 0:
                    pygame.draw.rect(
                        screen,
                        COLORS[block_element],
                        pos,
                        0,
                    )
