from dataclasses import dataclass
import re


print(__file__)

with open('day5/input.txt', 'r') as file:
    lines = file.read().splitlines()

_seeds, lines = lines[0].split(": ")[1].split(" "), lines[2:]
seeds: list[int] = list(map(int, _seeds))


@dataclass
class Mapping:
    destination: int
    source:      int
    length:      int


maps: dict[str, list[Mapping]] = dict()

current_map = None

for line in lines:
    if not line:
        continue

    match = re.match(r"(.+) map:", line)
    if match and (groups := match.groups()):
        current_map = groups[0]
        maps[current_map] = []
        continue

    values = list(map(int, line.split(" ")))

    maps[current_map].append(Mapping(*values))

mapping_order = [
    "seed-to-soil",
    "soil-to-fertilizer",
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location',
]


@lambda f: f()
def part1():
    def apply_map(source: int, map_name: str):
        for mapping in maps[map_name]:
            if mapping.source <= source < mapping.source + mapping.length:
                distance = source - mapping.source
                return mapping.destination + distance
        return source

    def apply_maps(source: int, map_names: list[str]):
        for map_name in map_names:
            source = apply_map(source, map_name)
        return source

    print(min(apply_maps(seed, mapping_order) for seed in seeds))


@lambda f: f()
def part2():
    def apply_map_range(range_start: int, range_length: int, map_name: str):
        mapped_ranges = []

        for mapping in maps[map_name]:
            intersection_start = max(mapping.source, range_start)
            intersection_end = min(mapping.source + mapping.length, range_start + range_length)
            intersection_length = intersection_end - intersection_start

            if intersection_length <= 0:
                continue

            mapped_ranges.append((intersection_start, intersection_end))

            distance = intersection_start - mapping.source
            # distance = 0
            yield mapping.destination + distance, intersection_length

        if not mapped_ranges:
            # if no mapping found the values stay the same
            yield range_start, range_length
            return

        mapped_ranges.sort(key=lambda x: x[0], reverse=False)

        # merge ranges
        i = 0
        while i < len(mapped_ranges) - 1:
            left, right = mapped_ranges[i], mapped_ranges[i + 1]

            if left[0] >= right[0]:
                mapped_ranges[i] = (left[0], max(sum(left), right[0]))
                del mapped_ranges[i + 1]
                continue
            i += 1

        next_range_start = range_start

        for mapped_range in mapped_ranges:
            if mapped_range[0] - next_range_start > 0:
                yield next_range_start, mapped_range[0] - next_range_start
            next_range_start = sum(mapped_range)

        if next_range_start < range_start + range_length:
            yield next_range_start, range_start + range_length - next_range_start

    def apply_maps_range(range_start: int, range_length: int, map_names: list[str]):
        if not map_names:
            yield range_start, range_length
            return  # range_start, range_length

        map_name, *map_names = map_names
        # print(map_name, range_start, range_length)
        for destination, length in apply_map_range(range_start, range_length, map_name):
            # print(destination, length)
            yield from apply_maps_range(destination, length, map_names)

    location_ranges = [list(apply_maps_range(x, y, mapping_order)) for x, y in zip(seeds[::2], seeds[1::2])]

    location_starts = [list(map(lambda x: x[0], location_range)) for location_range in location_ranges]

    print(min(map(min, location_starts)))

