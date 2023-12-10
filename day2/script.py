import functools
import re

print(__file__)

with open("day2/input.txt", "r") as f:
    lines = f.read().splitlines()
    id_sum = 0
    power_sum = 0

    possible_packages = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    # 12 reds, 13 greens, 14 blues
    for i, line in enumerate(lines):
        game_id, subsets = line.split(': ')
        game_id = int(game_id[5:])

        sets = subsets.split('; ')

        min_req_packages = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

        possible = True

        for subset in sets:
            for item in subset.split(', '):
                amount, color = item.split(' ')
                amount = int(amount)
                if min_req_packages[color] < amount:
                    min_req_packages[color] = amount
                if amount > possible_packages[color]:
                    possible = False
        power = functools.reduce(int.__mul__, min_req_packages.values())
        power_sum += power
        if possible:
            id_sum += game_id
    print(id_sum)
    print(power_sum)
