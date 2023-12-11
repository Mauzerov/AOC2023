import dataclasses

print(__file__)


@dataclasses.dataclass(slots=True)
class Galaxy:
    x: int
    y: int


for expansion in [2, 1_000_000]:
    with open("day11/input.txt") as f:
        lines = f.read().splitlines()

        # find all galaxies in the universe
        galaxies: list[Galaxy] = [
            Galaxy(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "#"
        ]

    number_of_galaxies = len(galaxies)

    # Sort the galaxies by x-axis
    galaxies = sorted(galaxies, key=lambda g: g.x)
    # Expand the universe on x-axis
    for i, galaxy in enumerate(galaxies[:-1], start=1):
        empty_spaces = galaxies[i].x - galaxy.x - 1
        # skip if there are no empty spaces
        if empty_spaces < 1:
            continue
        for j in range(i, number_of_galaxies):
            # increase the distance between galaxies by expansion - 1
            galaxies[j].x += empty_spaces * expansion - empty_spaces

    # Sort the galaxies by y-axis
    galaxies = sorted(galaxies, key=lambda g: g.y)
    # Expand the universe on y-axis
    for i, galaxy in enumerate(galaxies[:-1], start=1):
        empty_spaces = galaxies[i].y - galaxy.y - 1
        if empty_spaces < 1:
            continue
        for j in range(i, number_of_galaxies):
            galaxies[j].y += empty_spaces * expansion - empty_spaces

    sum_of_distances = 0
    for i, galaxy in enumerate(galaxies, start=1):
        # for each unique pair of galaxies, calculate the distance
        for j in range(i, number_of_galaxies):
            # Manhattan distance, because we can only move in 4 directions
            distance_x, distance_y = abs(galaxy.x - galaxies[j].x), abs(galaxy.y - galaxies[j].y)
            distance = distance_x + distance_y
            sum_of_distances += distance

    print(sum_of_distances)
