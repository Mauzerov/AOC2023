from pprint import pprint


print(__file__)


def string_differences(a: str, b: str) -> int:
    invalid = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            invalid += 1
    return invalid


with open('day13/input.txt', 'r') as f:
    patterns = [
        pattern.splitlines() for pattern in f.read().split('\n\n')
    ]


def find_mirror_location(pattern) -> tuple[tuple[int, int], ...]:
    mirror_location = None
    fixed_mirror_location = None

    for y in range(1, len(pattern)):
        bottom = pattern[y:y + y]
        top = pattern[y - len(bottom):y][::-1]

        differences = string_differences(''.join(bottom), ''.join(top))

        if differences == 0:
            mirror_location = 0, y
        elif differences == 1:
            fixed_mirror_location = 0, y

    if mirror_location and fixed_mirror_location:
        return mirror_location, fixed_mirror_location

    for x in range(1, len(pattern[0])):
        right = [pattern[y][x:x + x][::-1] for y in range(len(pattern))]
        left = [pattern[y][x - len(right[0]):x] for y in range(len(pattern))]

        differences = string_differences(''.join(left), ''.join(right))

        if differences == 0:
            mirror_location = x, 0
        elif differences == 1:
            fixed_mirror_location = x, 0

    if mirror_location and fixed_mirror_location:
        return mirror_location, fixed_mirror_location

    raise RuntimeError('Unreachable: No mirror location found')


summary = 0
fixed_summary = 0
for pattern in patterns:
    (mirror_x, mirror_y), (fixed_x, fixed_y) = find_mirror_location(pattern)
    summary += mirror_x + mirror_y * 100
    fixed_summary += fixed_x + fixed_y * 100

print(summary)
print(fixed_summary)

