import functools
from dataclasses import dataclass
import textwrap
from pprint import pprint
from time import perf_counter
import numpy as np

print(__file__)


@functools.lru_cache(maxsize=None)
def cached_sorted(_line) -> str: return ''.join(sorted(_line))


@functools.lru_cache(maxsize=None)
def cached_split(_line) -> list[str]: return _line.split('#')


@functools.lru_cache(maxsize=None)
def cached_reverse(_line) -> str: return ''.join(reversed(_line))


@dataclass(slots=True)
class Stack:
    start: int = 0
    size: int = 0


with open('day14/input.txt', 'r') as f:
    lines = tuple(f.read().splitlines())
    size = len(lines)


def calculate_total_load(_lines: np.array) -> int:
    global size, size
    total_load = 0

    stacks = [Stack(start=size) for _ in range(size)]

    for y, line in enumerate(_lines):
        for i, char in enumerate(line):
            if char == '#':
                arithmetic_sum = stacks[i].size * (2 * stacks[i].start - stacks[i].size + 1) // 2
                total_load += arithmetic_sum
                stacks[i].start = size - y - 1
                stacks[i].size = 0
            elif char == 'O':
                stacks[i].size += 1

    for stack in stacks:
        arithmetic_sum = stack.size * (2 * stack.start - stack.size + 1) // 2
        total_load += arithmetic_sum

    return total_load


print(calculate_total_load(lines))


@functools.lru_cache(maxsize=None)
def rotate(_lines: tuple[str]) -> tuple[str]:
    return tuple(
        cached_reverse(_line)
        for _line in zip(*_lines)
    )


@functools.lru_cache(maxsize=None)
def sort_line(_line: str) -> str:
    return '#'.join(cached_sorted(p) for p in cached_split(_line))


@functools.lru_cache(maxsize=None)
def apply_gravity(_lines: tuple[str]) -> tuple[str]:
    return tuple(
        sort_line(_line)
        for _line in _lines
    )


@functools.lru_cache(maxsize=None)
def spin_cycle(_lines: tuple[str]) -> tuple[str]:
    for _ in range(4):
        _lines = apply_gravity(rotate(_lines))
    return _lines


cache: dict[tuple[str, ...], int] = dict()
iterations = 0

while True:
    # key = ''.join(''.join(line) for line in lines)
    if lines in cache:
        first = cache[lines]
        billionth = ((1_000_000_000 - first) % (iterations - first))

        for key, value in cache.items():
            if value == first + billionth:
                load = 0
                for i, line in enumerate(key):
                    load += (size - i) * line.count('O')
                print(load)  # , value, billionth, first, iterations, iterations - first
        break
    cache[lines] = iterations
    iterations += 1
    start = perf_counter()
    lines = spin_cycle(lines)


