import pygame
import random
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
Oblock = [
    [3, 3,], 
    [3, 3,],
]
Sblock = [
    [4, 0,], 
    [4, 4,],
    [0, 4,],
]
ISblock = [
    [0, 5,], 
    [5, 5,],
    [5, 0,],
]

Lblock = [
    [6, 0,], 
    [6, 0,],
    [6, 6,],
]
Iblock = [
    [0, 7,], 
    [0, 7,],
    [7, 7,],
]

class World:
    """Class that defines the world in which the agents will live.
    The world size is of 300x600 by default and contains 20 rows by 10 columns with a cell size of 30.
    """

    def __init__(self) -> None:
        self.end = False
        self.rows = 20
        self.columns = 10
        self.cell_size = 30
        self.score = 0
        self.size = (self.columns * self.cell_size, self.rows * self.cell_size)

        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.grid[-1] = [1 for _ in range(self.columns)]
        self.grid[-1][0] = 0

        self.next_block = random.choice([Tblock, Oblock, Sblock, ISblock, Lblock, Iblock])
        self.block = random.choice([Tblock, Oblock, Sblock, ISblock, Lblock, Iblock])
        self.block_offset = [int(self.columns/2)-1, 0]

    def rotate(self):
        before_state = self.block
        self.block = list(zip(*self.block[::-1]))
        if self.detect_collision():
            self.block = before_state

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
            self.clear_rows()

            self.block = self.next_block
            self.next_block = random.choice([Tblock, Oblock, Sblock, ISblock, Lblock, Iblock])
            self.block_offset = [int(self.columns/2)-1, 0]

    def clear_rows(self):
        for i, row in enumerate(self.grid):
            if all(row):
                self.grid.pop(i)
                self.grid.insert(0, [0 for _ in range(self.columns)])
                self.score += self.columns
                print(self.score)

    def fix_block(self):
        if self.block_offset[1] <= len(self.block[1]):
            self.end = True
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
        # Draw next block
        for i, block_row in enumerate(self.next_block):
            for j, block_element in enumerate(block_row):
                pos = (
                    j * self.cell_size + SCREEN_RESOLUTION[0] / 1.9 + self.size[0] / 2 + self.cell_size,
                    i * self.cell_size + SCREEN_RESOLUTION[1] / 2 - self.size[1] / 2 + self.cell_size,
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
        # Draw current block
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
