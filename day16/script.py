from queue import Queue

print(__file__)


with open('day16/input.txt') as f:
    grid = f.read().splitlines()
    size = len(grid)
    assert size == len(grid[0])

global_visited = set()


# def timed(f):
#     from time import perf_counter
#
#     def wrapper(*args, **kwargs):
#         start = perf_counter()
#         result = f(*args, **kwargs)
#         end = perf_counter()
#         print(f'{f.__name__} took {end - start:.15f} seconds', result, args)
#         return result
#     return wrapper
#
#
# @timed
def move_beam(start: tuple[int, ...]) -> int:
    visited = set()
    to_visit = list()
    to_visit.append(start)
    while to_visit:
        beam = to_visit.pop()
        x, y, dx, dy = beam
        if x < 0 or y < 0 or x >= size or y >= size or beam in visited:
            continue
        visited.add(beam)
        if grid[y][x] == '.':
            to_visit.append((x + dx, y + dy, dx, dy))
            continue
        elif grid[y][x] == '/':
            dy, dx = -dx, -dy
        elif grid[y][x] == '\\':
            dy, dx = dx, dy
        elif grid[y][x] in '|-':
            if grid[y][x] == '|' and dx != 0:
                to_visit.append((x, y + 1, 0, 1))
                to_visit.append((x, y - 1, 0, -1))
                continue
            elif grid[y][x] == '-' and dy != 0:
                to_visit.append((x + 1, y, 1, 0))
                to_visit.append((x - 1, y, -1, 0))
                continue
            to_visit.append((x + dx, y + dy, dx, dy))
            continue
        else:
            raise RuntimeError('Unreachable')
        to_visit.append((x + dx, y + dy, dx, dy))

    unique_visited = set((x, y) for x, y, _, _ in visited)
    global_visited.update(unique_visited)
    return len(unique_visited)


print(move_beam((0, 0, 1, 0)))
maximum = 0
for i in range(size):
    if (0, i) not in global_visited:
        maximum = max(maximum, move_beam((0, i, 1, 0)))
    if (i, 0) not in global_visited:
        maximum = max(maximum, move_beam((i, 0, 0, 1)))
    if (size - 1, i) not in global_visited:
        maximum = max(maximum, move_beam((size - 1, i, 0, -1)))
    if (i, size - 1) not in global_visited:
        maximum = max(maximum, move_beam((i, size - 1, -1, 0)))

print(maximum)
