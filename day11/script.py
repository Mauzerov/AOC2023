import dataclasses

print(__file__)


@dataclasses.dataclass
class Galaxy:
    x: int
    y: int


for expansion in [2, 1_000_000]:
    with open("day11/input.txt") as f:
        lines = f.read().splitlines()

        galaxies: list[Galaxy] = [
            Galaxy(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "#"
        ]

    number_of_galaxies = len(galaxies)

    galaxies = sorted(galaxies, key=lambda g: g.x)

    for i, galaxy in enumerate(galaxies, start=1):
        if i == number_of_galaxies:
            break
        empty_spaces = galaxies[i].x - galaxy.x - 1
        if empty_spaces < 1:
            continue
        for j in range(i, len(galaxies)):
            galaxies[j].x += empty_spaces * expansion - empty_spaces

    galaxies = sorted(galaxies, key=lambda g: g.y)

    for i, galaxy in enumerate(galaxies, start=1):
        if i == number_of_galaxies:
            break
        empty_spaces = galaxies[i].y - galaxy.y - 1
        if empty_spaces < 1:
            continue
        for j in range(i, len(galaxies)):
            galaxies[j].y += empty_spaces * expansion - empty_spaces

    sum_of_distances = 0

    for i, galaxy in enumerate(galaxies, start=1):
        for j in range(i, len(galaxies)):
            distance_x, distance_y = abs(galaxy.x - galaxies[j].x), abs(galaxy.y - galaxies[j].y)
            distance = distance_x + distance_y
            sum_of_distances += distance

    print(sum_of_distances)
