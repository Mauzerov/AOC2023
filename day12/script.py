from dataclasses import dataclass
from pprint import pprint
import re
from functools import lru_cache

print(__file__)


@dataclass
class Spring:
    condition: str
    sizes: tuple[int, ...]


with open('day12/input.txt', 'r') as file:
    lines = file.read().splitlines()

    springs = [
        Spring(
            condition,
            tuple(int(size) for size in sizes.split(','))
        ) for condition, sizes in map(str.split, lines)
    ]


@lru_cache(maxsize=None)
def spring_combinations(condition: str, sizes: tuple[int, ...], start: int = 0) -> int:
    combination = 0
    if not sizes:
        return '#' not in condition[start:]

    size, *sizes = sizes
    for i in range(start, len(condition) - size + 1):
        if '#' in condition[start:i]:
            break
        # if gap between pots
        if '.' in condition[i:i+size]:
            continue
        # if either side of the spring is known
        if i > 0 and condition[i - 1] == '#':
            continue
        if i + size < len(condition) and condition[i + size] == '#':
            continue
        # print(" " * start, condition[:i], '(', condition[i:i+size], ')', condition[i+size:], sep='')

        combination += spring_combinations(condition, tuple(sizes), i + size + 1)
    return combination


sum_of_combinations = 0
sum_of_unfolded_combinations = 0

for spring in springs:
    comb = spring_combinations(spring.condition, spring.sizes)
    sum_of_combinations += comb

    sum_of_unfolded_combinations += spring_combinations(
        '?'.join([spring.condition] * 5),
        spring.sizes * 5
    )

print(sum_of_combinations)
print(sum_of_unfolded_combinations)
