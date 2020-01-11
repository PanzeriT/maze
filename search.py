from __future__ import annotations
from typing import TypeVar, Generic, List, Optional, Callable, Set

T: TypeVar = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def is_empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, data: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0):
        self.data: T = data
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial: T, end_test: Callable[[T], bool], next_steps: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # in frontier are all fields, we still have to check
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # in the set (to prevent duplicates) are all fields, which have already been checked
    explored: Set[T] = {initial}

    # loop as long there are fields left in the stack
    while not frontier.is_empty:
        current_node: Node[T] = frontier.pop()
        current_data: T = current_node.data
        # check, if we reached the end
        if end_test(current_data):
            return current_node
        # move through possible fields which haven't been explored yet
        for step in next_steps(current_data):
            # go to the next field, if the current was already checked
            if step in explored:
                continue
            explored.add(step)
            frontier.push(Node(step, current_node))
    return None


def nodes_in_path(node: Node[T]) -> List[Node[T]]:
    path: List[T] = [node.data]
    # go backwards to the start
    while node.parent is not None:
        node = node.parent
        path.append(node.data)
    path.reverse()
    return path
