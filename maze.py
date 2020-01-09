from enum import Enum
from typing import List, NamedTuple
import random


class Cell(str, Enum):
    EMPTY = ' '
    BLOCKED = '\u25a0'
    START = 'S'
    END = 'E'
    PATH = '*'


class Location(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 20, columns: int = 100, blockade_probability: float = 0.3,
                 start: Location = Location(0, 0), end: Location = Location(19, 99)):
        self._rows: int = rows
        self._columns: int = columns
        self.start: Location = start
        self.end: Location = end
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        self.add_blocks(rows, columns, blockade_probability)
        self._grid[start.row][start.column] = Cell.START
        self._grid[end.row][end.column] = Cell.END

    def add_blocks(self, rows: int, columns: int, blockade_probability: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < blockade_probability:
                    self._grid[row][column] = Cell.BLOCKED

    def __str__(self):
        output = ''
        for row in self._grid:
            output += ''.join([c.value for c in row]) + '\n'
        return output


if __name__ == '__main__':
    m = Maze()
    print(m)
