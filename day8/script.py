print(__file__)


with open("day8/input.txt") as f:
    lines = f.read().splitlines()
    dirs, _, *mapping_list = lines
    mapping = dict()
    for line in mapping_list:
        label, dest = line.split(" = ")
        left, right = dest[1:-1].split(", ")

        mapping[label] = (left, right)

current = "AAA"
moves = 0

while current != "ZZZ":
    move = dirs[moves % len(dirs)]
    print(move, current, mapping[current], moves)
    current = mapping[current][move == "R"]
    moves += 1

print(moves)


