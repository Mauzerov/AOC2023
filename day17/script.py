from typing import TypeAlias
from collections import defaultdict, deque
from heapq import heappush, heappop

print(__file__)

Point: TypeAlias = tuple[int, int]


def valid(_x, _y):
    return 0 <= _x < n and 0 <= _y < n


with open('day17/input.txt') as f:
    grid: list[list[int]] = [list(map(int, digits)) for digits in f.read().splitlines()]
    n = len(grid[0])


def smallest_heat_loss(min: int, max: int):
    # part 1
    visited = set()
    queue = [(0, 0, 0, 0, 0, 0)]
    while queue:
        heat_loss, x, y, dx, dy, steps = heappop(queue)

        if x == n - 1 and y == n - 1 and steps >= min:
            return heat_loss

        if (x, y, dx, dy, steps) in visited:
            continue
        visited.add((x, y, dx, dy, steps))

        if steps < max and (dx, dy) != (0, 0):
            nx, ny = x + dx, y + dy
            if valid(nx, ny):
                heappush(queue, (heat_loss + grid[ny][nx], nx, ny, dx, dy, steps + 1))

        if dx == 0 and dy == 0:  # at start
            for dx, dy in [(0, 1), (1, 0)]:  # try going down and right at start
                nx, ny = x + dx, y + dy
                if valid(nx, ny):
                    heappush(queue, (heat_loss + grid[ny][nx], nx, ny, dx, dy, 1))
        elif steps >= min:  # try rotating
            dx, dy = dy, dx  # rotate 90 degrees
            nx, ny = x + dx, y + dy

            if valid(nx, ny):
                heappush(queue, (heat_loss + grid[ny][nx], nx, ny, dx, dy, 1))

            dx, dy = -dx, -dy  # rotate 180 degrees
            nx, ny = x + dx, y + dy

            if valid(nx, ny):
                heappush(queue, (heat_loss + grid[ny][nx], nx, ny, dx, dy, 1))


print(smallest_heat_loss(0, 3))
print(smallest_heat_loss(4, 10))
