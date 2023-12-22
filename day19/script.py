import re
from dataclasses import dataclass, asdict, astuple
from functools import lru_cache

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


with open('input.txt') as f:
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


combination = {
    "x": (1, 4000),
    "m": (1, 4000),
    "a": (1, 4000),
    "s": (1, 4000),
}


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

combinations = 1

for key, value in combination.items():
    combinations *= value[1] - value[0] + 1

print(combinations)
