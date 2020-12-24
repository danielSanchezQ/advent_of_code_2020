from collections import defaultdict
from functools import reduce
from enum import Enum, auto

directions = {'e', 'w', 'ne', 'nw', 'se', 'sw'}


def parse_line(l):
    item = ""
    for next_item in l:
        item += next_item
        if item in directions:
            yield item
            item = ""


def parse_data(f):
    return (parse_line(l.rstrip()) for l in f)


# hexagonal coordinate system from: https://math.stackexchange.com/a/2643016
movements = {
    'e': (1, -1, 0),
    'w': (-1, 1, 0),
    'ne': (1, 0, -1),
    'nw': (0, 1, -1),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1)
}


def add_v(v1, v2):
    return tuple(sum(val) for val in zip(v1, v2))


class Tile(Enum):
    White = auto()
    Black = auto()


def solve_1(data):
    space = defaultdict(lambda: Tile.White)
    for l in data:
        position = reduce(add_v, map(movements.get, l), (0, 0, 0))
        space[position] = Tile.Black if space[position] == Tile.White else Tile.White
    return sum(1 for v in space.values() if v == Tile.Black)


if __name__ == "__main__":
    with open("./input/advent24.txt") as f:
        data_gen = parse_data(f)
        data = [list(e) for e in data_gen]
        print(solve_1(data))