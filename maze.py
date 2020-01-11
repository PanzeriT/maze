from enum import Enum
from typing import List, NamedTuple, Optional
import random

from search import Node, dfs, bfs, nodes_in_path


class Cell(str, Enum):
    EMPTY = ' '
    BLOCKED = '\u2588'
    START = 'S'
    END = 'E'
    PATH = '*'


class Location(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 25, columns: int = 250, blockade_probability: float = 0.3,
                 start: Location = Location(0, 0), end: Location = Location(24, 249)):
        self._rows: int = rows
        self._columns: int = columns
        self.start: Location = start
        self.end: Location = end
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        self.add_blocks(rows, columns, blockade_probability)
        self._grid[start.row][start.column] = Cell.START
        self._grid[end.row][end.column] = Cell.END

    def __str__(self):
        output = ''
        for row in self._grid:
            output += ''.join([c.value for c in row]) + '\n'
        return output

    def add_blocks(self, rows: int, columns: int, blockade_probability: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < blockade_probability:
                    self._grid[row][column] = Cell.BLOCKED

    def is_end(self, location: Location) -> bool:
        return location == self.end

    def next_steps(self, location: Location) -> List[Location]:
        locations: List[Location] = []
        if location.row + 1 < self._rows and self._grid[location.row + 1][location.column] != Cell.BLOCKED:
            locations.append(Location(location.row + 1, location.column))
        if location.row - 1 >= 0 and self._grid[location.row - 1][location.column] != Cell.BLOCKED:
            locations.append(Location(location.row - 1, location.column))
        if location.column + 1 < self._columns and self._grid[location.row][location.column + 1] != Cell.BLOCKED:
            locations.append(Location(location.row, location.column + 1))
        if location.column - 1 >= 0 and self._grid[location.row][location.column - 1] != Cell.BLOCKED:
            locations.append(Location(location.row, location.column - 1))
        return locations

    def print_path(self, path: List[Location]) -> None:
        for location in path:
            self._grid[location.row][location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.end.row][self.end.column] = Cell.END

    def delete_path(self, path: List[Location]) -> None:
        for location in path:
            self._grid[location.row][location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.end.row][self.end.column] = Cell.END


if __name__ == '__main__':
    m: Maze = Maze()

    # Solve the Maze with DFS
    dfs_solution: Optional[Node[Location]] = dfs(m.start, m.is_end, m.next_steps)
    if dfs_solution is None:
        print(m)
        print('No solution found with depth-first search.')
    else:
        dfs_path: List[Location] = nodes_in_path(dfs_solution)
        m.print_path(dfs_path)
        print(m)
        print(f'Maze can be solved with depth-first search in {len(dfs_path)} steps.\n\n')
        m.delete_path(dfs_path)

    # Solve the Maze with BFS
    bfs_solution: Optional[Node[Location]] = bfs(m.start, m.is_end, m.next_steps)
    if bfs_solution is None:
        print('No solution found with breadth-first search.')
    else:
        bfs_path: List[Location] = nodes_in_path(bfs_solution)
        m.print_path(bfs_path)
        print(m)
        print(f'Maze can be solved with breadth-first search in {len(bfs_path)} steps.\n\n')
        m.delete_path(bfs_path)
