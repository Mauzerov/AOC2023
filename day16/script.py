from typing import NamedTuple
from queue import Queue


class Beam(NamedTuple):
    x: int
    y: int
    dx: int
    dy: int


print(__file__)


with open('day16/input.txt') as f:
    grid = f.read().splitlines()
    size = len(grid)
    assert size == len(grid[0])


start = Beam(0, 0, 1, 0)

global_visited = set()


def move_beam(start: Beam) -> int:
    visited = set()
    to_visit = Queue()
    to_visit.put(start)

    while not to_visit.empty():
        beam = to_visit.get()

        if beam in visited or beam.x < 0 or beam.y < 0 or beam.x >= size or beam.y >= size:
            continue

        visited.add(beam)
        x, y, dx, dy = beam

        if grid[y][x] == '.':
            to_visit.put(Beam(x + dx, y + dy, dx, dy))
            continue

        if grid[y][x] in '|-':
            # return Beam(x + dx, y + dy, dx, dy)
            if grid[y][x] == '|' and dx != 0:
                to_visit.put(Beam(x, y + 1, 0, 1))
                to_visit.put(Beam(x, y - 1, 0, -1))
                continue
            elif grid[y][x] == '-' and dy != 0:
                to_visit.put(Beam(x + 1, y, 1, 0))
                to_visit.put(Beam(x - 1, y, -1, 0))
                continue
            to_visit.put(Beam(x + dx, y + dy, dx, dy))
            continue

        if grid[y][x] == '/':
            match (dx, dy):
                case (1, 0):  # right -> up
                    dx, dy = 0, -1
                case (-1, 0):  # left -> down
                    dx, dy = 0, 1
                case (0, 1):  # down -> left
                    dx, dy = -1, 0
                case (0, -1):  # up -> right
                    dx, dy = 1, 0

        elif grid[y][x] == '\\':
            match (dx, dy):
                case (1, 0):
                    dx, dy = 0, 1
                case (-1, 0):
                    dx, dy = 0, -1
                case (0, 1):
                    dx, dy = 1, 0
                case (0, -1):
                    dx, dy = -1, 0

        else:
            raise RuntimeError('Unreachable')

        to_visit.put(Beam(x + dx, y + dy, dx, dy))

    unique_visited = set((x, y) for x, y, _, _ in visited)
    global_visited.update(unique_visited)
    return len(unique_visited)


print(move_beam(start))

maximum = 0

for i in range(size):
    if (0, i) not in global_visited:
        maximum = max(maximum, move_beam(Beam(0, i, 1, 0)))
    if (i, 0) not in global_visited:
        maximum = max(maximum, move_beam(Beam(i, 0, 0, 1)))
    if (size - 1, i) not in global_visited:
        maximum = max(maximum, move_beam(Beam(size - 1, 0, 0, -1)))
    if (i, size - 1) not in global_visited:
        maximum = max(maximum, move_beam(Beam(0, size - 1, -1, 0)))

print(maximum)
