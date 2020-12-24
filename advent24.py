from collections import defaultdict
from functools import reduce
from enum import Enum, auto
import itertools

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
    return space


def calc_blacks(space):
    return sum(1 for v in space.values() if v == Tile.Black)


def rule_black(coords, space):
    adjacent_black_tiles = sum(1 for other in movements.values() if space[add_v(coords, other)] == Tile.Black)
    if adjacent_black_tiles == 0 or adjacent_black_tiles > 2:
        return Tile.White
    return Tile.Black


def rule_white(coords, space):
    adjacent_black_tiles = sum(1 for other in movements.values() if space[add_v(coords, other)] == Tile.Black)
    if adjacent_black_tiles == 2:
        return Tile.Black
    return Tile.White


def space_blacks(space):
    return [coord for coord, tile in space.items() if tile == Tile.Black]


def space_whites(space, blacks=None):
    blacks = blacks or space_blacks(space)
    return set(itertools.chain.from_iterable(
        (coord for v2 in movements.values() if space[(coord := add_v(v1, v2))] == Tile.White) for v1 in blacks
    ))


def solve_2(data, n):
    space = solve_1(data)
    for _ in range(n):
        new_space = defaultdict(lambda: Tile.White)
        blacks = space_blacks(space)
        whites = space_whites(space, blacks)
        for black_coords in blacks:
            new_space[black_coords] = rule_black(black_coords, space)
        for white_coords in whites:
            new_space[white_coords] = rule_white(white_coords, space)
        space = new_space
    return space


if __name__ == "__main__":
    with open("./input/advent24.txt") as f:
        data_gen = parse_data(f)
        data = [list(e) for e in data_gen]
        print(calc_blacks(solve_1(data)))
        print(calc_blacks(solve_2(data, 100)))