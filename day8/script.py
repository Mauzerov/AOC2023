from math import lcm

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
    current = mapping[current][move == "R"]
    moves += 1

print(moves)
# Part 2
nodes = list(filter(lambda x: x[-1] == "A", mapping.keys()))
moves = [0] * len(nodes)

while any(map(lambda x: x[-1] != "Z", nodes)):
    for i, node in enumerate(nodes):
        if node[-1] == "Z":
            continue
        move = dirs[moves[i] % len(dirs)]
        nodes[i] = mapping[node][move == "R"]
        moves[i] += 1
print(lcm(*moves))
