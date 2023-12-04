import re
from pprint import pprint
print(__file__)


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

lines = map(lambda line: line.split(': ')[1], lines)

total = 0

card_copies = dict()
for index, line in enumerate(lines):
    winning, my = line.split(' | ')
    
    winning = re.split(r'\s+', winning)
    my = re.split(r'\s+', my)
    winning = list(filter(lambda x: len(x), winning))
    
    matches = set(winning) & set(my)
    matches = len(matches) - ('' in my and '' in winning)
    card_copies[index] = card_copies.get(index, 0) + 1
    for i in range(index + 1, matches + index + 1):
        card_copies[i] = card_copies.get(i, 0) + card_copies[index]
    pprint(index)
    pprint(card_copies)
    # print(set(winning) & set(my))
    if matches:
        total += 2 ** (matches - 1)
        

print(total)

print(sum(card_copies.values()))

