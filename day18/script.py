import re
from dataclasses import dataclass, field
from typing import NamedTuple

print(__file__)


@dataclass(slots=True)
class Node:
    x: int
    y: int
    next_dir: str = None

    next: 'Node' = field(repr=False, default=None)

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y


DIRECTIONS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
    '0': (1, 0),
    '1': (0, 1),
    '2': (-1, 0),
    '3': (0, -1),
}

DigPlan = NamedTuple('DigPlan', [('direction', str), ('distance', str), ('color', str)])

with open('day18/input.txt') as f:
    plans: list[DigPlan] = [
        DigPlan(*re.search(r'([LURD]) (\d+) \(#([a-f0-9]{6})\)', line).groups())
        for line in f.read().splitlines()
    ]


def shoelace_formula(node: Node) -> float:
    dx, dy = lowest_xy(node)
    dx, dy = abs(dx) + 1, abs(dy) + 1
    start = curr = node
    area = 0
    while start != curr.next:
        # shoe lace formula
        area += (curr.x + dx) * (curr.next.y + dy) - (curr.y + dy) * (curr.next.x + dx)
        # add edge
        area += abs(curr.x - curr.next.x) + abs(curr.y - curr.next.y)
        curr = curr.next

    # add last edge
    area += (curr.x + dx) * (curr.next.y + dy) - (curr.y + dy) * (curr.next.x + dx)
    area += abs(curr.x - curr.next.x) + abs(curr.y - curr.next.y)

    return area // 2 + 1  # +1 for the last corner


def lowest_xy(node: Node) -> tuple[int, int]:
    start = curr = node
    x, y = float('inf'), float('inf')
    while start != curr.next:
        curr = curr.next
        x = min(x, curr.x)
        y = min(y, curr.y)
    return x, y


def parse_part1(_plans: list[DigPlan]) -> Node:
    start = Node(0, 0)
    node = start
    for plan in _plans:
        dx, dy = DIRECTIONS[plan.direction]
        node.next_dir = plan.direction
        distance = int(plan.distance)
        node.next = Node(
            node.x + dx * distance,
            node.y + dy * distance
        )
        node = node.next
    node.next = start
    return start


def parse_part2(_plans: list[DigPlan]) -> Node:
    start = Node(0, 0)
    node = start
    for plan in _plans:
        *distance_hex, direction = plan.color
        distance = int(''.join(distance_hex), 16)
        dx, dy = DIRECTIONS[direction]
        node.next_dir = direction
        node.next = Node(
            node.x + dx * distance,
            node.y + dy * distance,
        )
        node = node.next
    node.next = start
    return start


print(shoelace_formula(parse_part1(plans)))
print(shoelace_formula(parse_part2(plans)))
