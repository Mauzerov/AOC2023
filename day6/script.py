import functools
import math
from dataclasses import dataclass
import re

print(__file__)


@dataclass
class Race:
    duration: int
    distance: int

    def winning_ways(self) -> int:
        """
        mathematical formula:
            for n in 0..duration
            n * (duration - n) > distance
            n^2 - duration * n + distance < 0
        solution range:
            delta = duration^2 - 4 * distance
            n1 = (duration - sqrt(delta)) / 2  # smaller solution (rounded down)
            n2 = (duration + sqrt(delta)) / 2  # bigger solution (rounded up)

            n in (min(n1, n2), max(n1, n2))  # real solution range

            number of integer solutions between n1 and n2:
                n1 - n2 - 1
        :return:
        """
        duration, distance = self.duration, self.distance

        delta = duration ** 2 - 4 * distance

        n1 = (duration - delta ** 0.5) / 2
        n2 = (duration + delta ** 0.5) / 2
        n1, n2 = math.floor(n1), math.ceil(n2)

        return n2 - n1 - 1


with open('day6/input.txt', 'r') as f:
    lines = re.sub(r" +", " ", f.read()).splitlines()
    one_race = [
        int(''.join(re.findall(r'(\d+)', line)))
        for line in lines
    ]

winning_ways = [Race(int(t), int(d)).winning_ways()
                for t, d in zip(*map(lambda l: l.split(' ')[1:], lines))]

print(
    functools.reduce(int.__mul__, winning_ways)
)

print(Race(*one_race).winning_ways())


