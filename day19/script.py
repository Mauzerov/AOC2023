import re
from dataclasses import dataclass, asdict, astuple
from functools import lru_cache
from itertools import product
from pprint import pprint

print(__file__)


@dataclass(slots=True, frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


@dataclass(slots=True, frozen=True)
class System:
    name: str
    conditions: tuple[dict[str, str]]
    not_found: str


with open('day19/input.txt') as f:
    systems_input, parts_input = f.read().split("\n\n")

    systems = {}

    for system_line in systems_input.splitlines():
        system_name, conditions, _else =\
            re.search(r'([a-z]+)\{((?:[xmas][<>]\d+:[a-zAR]+,)+)([a-zAR]+)}', system_line).groups()

        *conditions, _ = conditions.split(",")
        conditions_dict: tuple[dict[str, str], ...] = tuple(
            eval(re.sub(r'(.+):(.+)', r'("\1","\2")', condition)) for condition in conditions
        )
        systems[system_name] = System(system_name, conditions_dict, _else)

    parts = [
        Part(**eval(re.sub(r'([xmas])=', r'"\1":', part))) for part in parts_input.splitlines()
    ]


@lru_cache(maxsize=None)
def traverse_systems(part: Part, system: System) -> bool:
    # Part 1
    for condition in system.conditions:
        condition, destination = condition
        for key, value in asdict(part).items():
            if key not in condition:
                continue

            if eval(condition.replace(key, str(value))):
                if destination.isupper():
                    return destination == 'A'
                return traverse_systems(part, systems[destination])

    if system.not_found.isupper():
        return system.not_found == 'A'
    return traverse_systems(part, systems[system.not_found])


accepted_sum = 0
for part in parts:
    if traverse_systems(part, systems["in"]):
        accepted_sum += sum(astuple(part))

print(accepted_sum)


def calculate_combinations(false_: list[str], true_: list[str]):
    bounds = {
        'x': set(),
        'm': set(),
        'a': set(),
        's': set(),
    }
    false_conditions, true_conditions = false_, true_

    for false_condition in false_conditions:
        key, op, value = re.search(r'([xmas])([<>])(\d+)', false_condition).groups()
        value = int(value)

        if op == '<':
            bounds[key].add(range(value, 4000))
        elif op == '>':
            bounds[key].add(range(1, value))

    for true_condition in true_conditions:
        key, op, value = re.search(r'([xmas])([<>])(\d+)', true_condition).groups()
        value = int(value)

        if op == '<':
            bounds[key].add(range(1, value - 1))
        elif op == '>':
            bounds[key].add(range(value + 1, 4000))

    distinct_bounds = {
        key: set(range(1, 4001)) for key in bounds.keys()
    }

    for key, value in bounds.items():
        for range_ in value:
            distinct_bounds[key] &= (set(range_) | {range_.stop})

    product_ = 1
    for key, value in distinct_bounds.items():
        product_ *= len(value)
    return product_


def calculate_bounds(system: System, false_conditions: list[str], true_conditions: list[str]):
    _possibilities = 0
    current_conditions = []
    for condition, destination in system.conditions:
        current_conditions.append(condition)
        if destination.islower():
            _possibilities += calculate_bounds(
                systems[destination],
                list(false_conditions + current_conditions[:-1]),
                list(true_conditions + [condition])
            )
            continue
        if destination == 'R':
            continue
        ## Acceptable Condition

        _possibilities += calculate_combinations(
            false_conditions + current_conditions[:-1],
            true_conditions + [condition]
        )

    ## Else Condition
    if system.not_found.islower():
        _possibilities += calculate_bounds(
            systems[system.not_found],
            list(false_conditions + current_conditions),
            true_conditions.copy()
        )
    elif system.not_found == 'R':
        pass
    else:  # Acceptable Condition
        _possibilities += calculate_combinations(
            false_conditions + current_conditions,
            true_conditions.copy()
        )

    return _possibilities


possibilities = calculate_bounds(systems["in"], [], [])

print(possibilities)
#
# combinations = 1
# for key, (min_, max_) in bounds.items():
#     combinations *= max_ - min_ + 1
#
# print(combinations)