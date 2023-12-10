import re
from pprint import pprint
print(__file__)


with open('day4/input.txt', 'r') as f:
    lines = f.read().splitlines()

lines = map(lambda l: l.split(': ')[1], lines)

total = 0

card_copies = dict()
for index, line in enumerate(lines):
    winning, my_numbers = line.split(' | ')

    # parse my number
    my_numbers = re.split(r'\s+', my_numbers.strip())

    # parse winning numbers
    winning = list(filter(lambda x: len(x), re.split(r'\s+', winning.strip())))

    matches = len(set(winning) & set(my_numbers))  # count matches
    card_copies[index] = card_copies.get(index, 0) + 1  # add the card itself
    for i in range(index + 1, matches + index + 1):
        card_copies[i] = card_copies.get(i, 0) + card_copies[index]  # add copies to next cards
    if matches:  # if there are matches, add 2^(matches - 1) to total
        # 2^(matches - 1) - value of card doubled for each match
        total += 2 ** (matches - 1)
        

print(total)
print(sum(card_copies.values()))

