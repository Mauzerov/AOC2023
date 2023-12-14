from dataclasses import dataclass
import textwrap
from time import perf_counter
import numpy as np

print(__file__)


@dataclass(slots=True)
class Stack:
    start: int = 0
    height: int = 0


with open('day14/input.txt', 'r') as f:
    lines = [list(line) for line in f.read().splitlines()]
    height = len(lines)
    width = len(lines[0])


def calculate_total_load(_lines: np.array) -> int:
    global height, width
    total_load = 0

    stacks = [Stack(start=height) for _ in range(width)]

    for y, line in enumerate(_lines):
        for i, char in enumerate(line):
            if char == '#':
                arithmetic_sum = stacks[i].height * (2 * stacks[i].start - stacks[i].height + 1) // 2
                total_load += arithmetic_sum
                stacks[i].start = height - y - 1
                stacks[i].height = 0
            elif char == 'O':
                stacks[i].height += 1

    for stack in stacks:
        arithmetic_sum = stack.height * (2 * stack.start - stack.height + 1) // 2
        total_load += arithmetic_sum

    return total_load


start = perf_counter()
print(calculate_total_load(lines))
print("(Part 2) Time taken:", perf_counter() - start)


def spin_cycle(_lines: list[list[str]]):
    global cache, width, height

    # Move North
    for y, line in enumerate(_lines):
        for i, char in enumerate(line):
            if char == 'O':
                for j in range(y - 1, -1, -1):
                    if _lines[j][i] != '.':
                        break
                    _lines[j][i], _lines[j + 1][i] = _lines[j + 1][i], _lines[j][i]

    # Move West
    for i in range(width):
        for j in range(height):
            if _lines[j][i] == 'O':
                for k in range(i - 1, -1, -1):
                    if _lines[j][k] != '.':
                        break
                    _lines[j][k], _lines[j][k + 1] = _lines[j][k + 1], _lines[j][k]

    # Move South
    for y in range(height - 1, -1, -1):
        for i in range(width):
            if _lines[y][i] == 'O':
                for j in range(y + 1, height):
                    if _lines[j][i] != '.':
                        break
                    _lines[j][i], _lines[j - 1][i] = _lines[j - 1][i], _lines[j][i]

    # Move East
    for i in range(width - 1, -1, -1):
        for j in range(height):
            if _lines[j][i] == 'O':
                for k in range(i + 1, width):
                    if _lines[j][k] != '.':
                        break
                    _lines[j][k], _lines[j][k - 1] = _lines[j][k - 1], _lines[j][k]


cache: dict[str, int] = dict()
iterations = 0
start = perf_counter()

while True:
    key = ''.join(''.join(line) for line in lines)
    # key = ''.join(''.join(line) for line in lines)
    if key in cache:
        first = cache[key]
        billionth = ((1_000_000_000 - first) % (iterations - first))

        for key, value in cache.items():
            if value == first + billionth:
                _lines = textwrap.wrap(key, width)
                load = 0
                for i, line in enumerate(_lines):
                    load += (height - i) * line.count('O')
                print(load, value, billionth, first, iterations, iterations - first)
        break
    cache[key] = iterations
    iterations += 1
    spin_cycle(lines)
print("(Part 2) Time taken:", perf_counter() - start)

