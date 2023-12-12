from pprint import pprint
from typing import TypeAlias
from operator import add
from collections import deque

print(__file__)

Connection: TypeAlias = tuple[int, int]

with open("day10/input.txt") as f:
    pipe_map = f.read().splitlines()
    dots = []
    start = None
    for y, line in enumerate(pipe_map):
        x = line.find("S")
        if x != -1:
            start = (x, y)


def pipe_at(x: int, y: int) -> str:
    return pipe_map[y][x]


pipes: dict[str, list[Connection]] = {
    "|": [(0, -1), (0, 1)],
    "-": [(-1, 0), (1, 0)],
    "L": [(0, -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "7": [(0, 1), (-1, 0)],
    "F": [(0, 1), (1, 0)],
}

pipes_pointing_to_start = list()
for x, y in set(item for sublist in pipes.values() for item in sublist):
    pipe = pipe_at(*map(add, start, (x, y)))
    if (x, y) in pipes[pipe]:
        pipes_pointing_to_start.extend(filter(lambda d: d != (x, y), pipes[pipe]))

start_symbol = None
for pipe, directions in pipes.items():
    if all(d in directions for d in pipes_pointing_to_start):
        start_symbol = pipe
        break

assert start_symbol is not None

current_position = start
direction = pipes[start_symbol][0]  # start going in the direction of the first pipe

pipe_length = 1
pipe_locations = set()
pipe_locations.add(start)

while pipe_at(*map(add, current_position, direction)) != "S":
    pipe_length += 1
    next_position = tuple(map(add, current_position, direction))
    pipe_locations.add(next_position)

    pipe_connections = pipes[pipe_at(*next_position)]

    next_direction, = filter(
        lambda d: current_position != tuple(map(add, next_position, d)),
        pipe_connections
    )

    current_position = next_position
    direction = next_direction

print(pipe_length // 2)  # PART 1

# filter out all pipes that are not on the main path
filtered_pipe_map = [
    ''.join(c if (x, y) in pipe_locations else "."
            for x, c in enumerate(line)).replace("S", start_symbol)
    for y, line in enumerate(pipe_map)
]

# expand the gaps between pipes to allow easier pathfinding / traversing
expanded_gaps = list()
for line in filtered_pipe_map:
    new_line = ""  # expanded x-axis
    next_line = ""  # expanded y-axis
    for i in range(len(line) - 1):
        new_line += line[i]
        if line[i] in 'FL-':
            new_line += "-"
        elif line[i] in 'J7|.':
            new_line += "."
        if line[i] in 'F7|':
            next_line += "|."
        elif line[i] in 'LJ-.':
            next_line += ".."
    expanded_gaps.append(list(new_line + line[-1]))
    expanded_gaps.append(list(next_line + line[-1]))


# find the bounds of the expanded grid
# we need to add/subtract 1 to allow traversing going around the edges
left = min(x * 2 for x, _ in pipe_locations) - 1
right = max(x * 2 for x, _ in pipe_locations) + 1
top = min(y * 2 for _, y in pipe_locations) - 1
bottom = max(y * 2 for _, y in pipe_locations) + 1

# traverse the expanded grid and fill in all the gaps connected to the outside
to_see = deque()
to_see.append((left, top))  # start in the top left corner where pipes can't be

while to_see:  # while there are still gaps to see
    x, y = to_see.pop()
    # traverse all 4 directions around the gap
    for i in (-1, 1):
        for j in (-1, 1):
            if x + i < left or x + i > right:
                continue
            if y + j < top or y + j > bottom:
                continue
            # if the gap is connected to the outside, fill it in and add it to the list of gaps to see
            if expanded_gaps[y + j][x + i] == '.':
                expanded_gaps[y + j][x + i] = "O"
                to_see.append((x + i, y + j))

# count the number of 2x2 squares of dots
# since we expanded the gaps, we need to check 2x2 squares
dots = 0
for x in range(left, right - 1, 2):
    for y in range(top, bottom - 1, 2):
        if all(c == '.' for c in expanded_gaps[y][x:x + 2] + expanded_gaps[y + 1][x:x + 2]):
            dots += 1

print(dots)  # PART 2
