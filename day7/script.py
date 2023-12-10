import dataclasses
import typing
from collections import Counter

print(__file__)


def map_label_to_value(label: str) -> int:
    return {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11 if Bet.strength_method is not Bet.hand_strength_jeepers else 1,
        'T': 10,
    }.get(label, None) or int(label)


@dataclasses.dataclass
class Bet:
    cards: str
    value: int

    strength_method: typing.Callable[[typing.Self, typing.Self], int] = None

    def occurrences(self) -> list[tuple[str, int]]:
        return Counter(self.cards).most_common()

    def hand_strength(self) -> int:
        occurrences = self.occurrences()
        if occurrences[0][1] >= 4:
            return 2 + occurrences[0][1]
        elif occurrences[0][1] == 3:
            return 5 if occurrences[1][1] == 2 else 4
        elif occurrences[0][1] == 2:
            return 3 if occurrences[1][1] == 2 else 2
        return 1

    def hand_strength_jeepers(self) -> int:
        occurrences = self.occurrences()
        jeepers = self.cards.count('J')

        if occurrences[0][0] == 'J':
            _, *occurrences = occurrences
            if len(occurrences) == 0:
                return 7

        strength = 1
        if occurrences[0][1] + jeepers >= 4:
            strength = 2 + occurrences[0][1] + jeepers
        elif occurrences[0][1] + jeepers == 3:
            strength = 5 if occurrences[1][1] == 2 else 4
        elif occurrences[0][1] + jeepers == 2:
            strength = 3 if occurrences[1][1] == 2 else 2
        return max(strength, self.hand_strength())

    def __lt__(self, other: typing.Self):
        strength = self.__class__.strength_method or self.__class__.hand_strength

        self_hand_strength = strength(self)
        other_hand_strength = strength(other)

        if self_hand_strength == other_hand_strength:
            for left, right in zip(self.cards, other.cards):
                if map_label_to_value(left) > map_label_to_value(right):
                    return False
                elif map_label_to_value(left) < map_label_to_value(right):
                    return True

        return self_hand_strength < other_hand_strength


with open('day7/input.txt') as f:
    lines = f.readlines()

    bets = list(
        map(
            lambda line: Bet(line.split(' ')[0], int(line.split(' ')[1])),
            lines
        )
    )

# Part 1
sorted_bets = sorted(bets)
total_winnings = 0

for i, bet in enumerate(sorted_bets, start=1):
    total_winnings += bet.value * i

print(total_winnings)

# Part 2
Bet.strength_method = Bet.hand_strength_jeepers

sorted_bets = sorted(bets)
total_winnings = 0

for i, bet in enumerate(sorted_bets, start=1):
    total_winnings += bet.value * i

print(total_winnings)
