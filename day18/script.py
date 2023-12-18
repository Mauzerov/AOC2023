import re
from typing import NamedTuple
from dataclasses import dataclass
import numpy as np
from collections import deque


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


DigPlan = NamedTuple('DigPlan', [('direction', str), ('distance', str), ('color', str)])

print(__file__)


with open('day18/input.txt') as f:
    plans: list[DigPlan] = [
        DigPlan(*re.search(r'([LURD]) (\d+) \(#([a-f0-9]{6})\)', line).groups())
        for line in f.read().splitlines()
    ]


directions = {
    'L': (-1, 0),
    'U': (0, -1),
    'R': (1, 0),
    'D': (0, 1),
}


position = (0, 0)
path = set()

for plan in plans:
    dx, dy = directions[plan.direction]

    for _ in range(int(plan.distance)):
        position = (position[0] + dx, position[1] + dy)
        path.add(Point(*position))


smallest_x = min(path, key=lambda p: p.x).x
smallest_y = min(path, key=lambda p: p.y).y

for point in path:
    point.x -= smallest_x - 1
    point.y -= smallest_y - 1

smallest_x = min(path, key=lambda p: p.x).x
smallest_y = min(path, key=lambda p: p.y).y
biggest_x = max(path, key=lambda p: p.x).x
biggest_y = max(path, key=lambda p: p.y).y
width, height = smallest_x + biggest_x + 1, smallest_y + biggest_y + 1

print(width, height)
print((smallest_x, smallest_y), (biggest_x, biggest_y))

path = [(point.x, point.y) for point in path]
grid = np.zeros((height, width), dtype=np.int8)

queue = deque([(0, 0)])
while queue:
    x, y = current = queue.popleft()

    if grid[y, x] != 0 or current in path:
        continue

    grid[y, x] = 1

    for dx, dy in directions.values():
        new_x, new_y = x + dx, y + dy

        if 0 <= new_y < height and width > new_x >= 0:
            queue.append((new_x, new_y))

print((height * width) - np.sum(grid))

for y in range(height):
    for x in range(width):
        if grid[y, x] == 0:
            print('#', end='')
        else:
            print('.', end='')
    print()