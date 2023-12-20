from dataclasses import dataclass, field
from typing import NamedTuple


DigPlan = NamedTuple('DigPlan', [('direction', str), ('distance', str), ('color', str)])


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))


@dataclass(slots=True)
class Node:
    x: int
    y: int
    next_dir: str = None

    next: 'Node' = field(repr=False, default=None)
    prev: 'Node' = field(repr=False, default=None)

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y


def left_up_most_node(node: Node) -> Node:
    result = start = node
    while node.next is not start:
        node = node.next
        if node.y < result.y or (node.y == result.y and node.x < result.x):
            result = node
    return result


def linked_size(node: Node) -> int:
    result = 0
    start = node
    while node.next is not start:
        result += 1
        node = node.next
    return result


DIRECTIONS = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
    '0': Point(1, 0),
    '1': Point(0, 1),
    '2': Point(-1, 0),
    '3': Point(0, -1),
}


def nodes_between(left: Node, right: Node) -> list[Node]:
    assert left.next is right and right.prev is left
    assert left.y == right.y and left.x < right.x

    result = []
    node = right
    while node is not left:
        node = node.next
        if left.x < node.x < right.x and left.y == node.y:
            result.append(node)
    return sorted(result, key=lambda n: n.x)

