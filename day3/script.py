import dataclasses
import functools
from pprint import pprint

print(__file__)


@dataclasses.dataclass
class Symbol:
    symbol: str
    x: int
    y: int

    def __hash__(self):
        return hash((self.symbol, self.x, self.y))


def is_part_number(_grid: list[str], _x: int, _y: int, _width: int):
    left, top = max(_x - 1, 0), max(_y - 1, 0)
    right, bottom = min(_x + _width, len(_grid[0]) - 1), min(_y + 1, len(_grid) - 1)
    _symbols = []
    for i in range(left, right + 1):
        for j in range(top, bottom + 1):
            # print('Checking:', _grid[j][i])
            if not _grid[j][i].isdigit() and _grid[j][i] != '.':
                # print('Checking:', _grid[_y][_x: _x + _width], 'result', True)
                _symbols.append(Symbol(_grid[j][i], i, j))
                # return True
    # print('Checking:', _grid[_y][_x: _x + _width], 'result', False)
    return _symbols
    # return False


with open("day3/input.txt", "r") as f:
    grid: list[str] = f.read().splitlines()
    gears: dict[Symbol, list[int]] = {}
    width, height = len(grid[0]), len(grid)
    sum_part_numbers = 0
    for y in range(height):
        x = 0
        while x < width:
            if not grid[y][x].isdigit():
                x += 1
                continue
            width_of_part = 1
            while grid[y][x:x + width_of_part].isdigit() and x + width_of_part <= width:
                width_of_part += 1
            number = int(grid[y][x:x + width_of_part - 1])
            symbols = is_part_number(grid, x, y, width_of_part - 1)
            if symbols:
                sum_part_numbers += number

                for gear in filter(lambda s: s.symbol == '*', symbols):
                    if gear not in gears:
                        gears[gear] = []
                    gears[gear].append(number)

            x += width_of_part

    print(sum_part_numbers)

    double_gears = filter(lambda g: len(gears[g]) > 1, gears)

    print(sum(map(lambda g: functools.reduce(int.__mul__, gears[g]), double_gears)))
