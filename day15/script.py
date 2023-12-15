from functools import lru_cache
from pprint import pprint
import re

print(__file__)

with open('day15/input.txt') as f:
    strings = f.read().rstrip().split(',')


@lru_cache(maxsize=None)
def hashify(string: str) -> int:
    current_value = 0
    for char in string:
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value


print(sum(hashify(string) for string in strings))


hashmap = dict()

for string in strings:
    groups = re.search(r'([a-z]+)([=\-])(\d?)', string).groups()

    label, operation, power = groups
    label_hash = hashify(label)

    array = hashmap.get(label_hash, list())
    hashmap[label_hash] = array
    if operation == '=':
        for i in range(len(array)):
            if re.match(f"^{label}=", array[i]):
                array[i] = string
                break
        else:
            array.append(string)
    elif operation == '-':
        to_remove = filter(lambda s: re.match(f"^{label}=", s), array)
        for rem in to_remove:
            array.remove(rem)
    else:
        assert False, f'Unreachable {string!r}'

focusing_power = 0
for label_hash, array in hashmap.items():
    for i, string in enumerate(array, start=1):
        *_, power = string
        focusing_power += (label_hash + 1) * int(power) * i

print(focusing_power)
