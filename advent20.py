import parse
import itertools
from collections import defaultdict
from math import prod
tile_id = "Tile {:d}:"


def parse_tile_data(f):
    id = parse.parse(tile_id, next(f))
    tile = [l.rstrip() for l in itertools.takewhile(lambda x: x != "\n", f)]
    return id[0], tile


def parse_input(f):
    try:
        while True:
            yield Tile(*parse_tile_data(f))
    except StopIteration:
        return


class Tile(object):
    __slots__ = ["id", "tile_size", "up", "down", "left", "right"]

    def __init__(self, id, tile_data):
        self.id = id
        self.tile_size = len(tile_data)
        self._load_sides(tile_data)

    def _load_sides(self, tile_data):
        self.up = list(tile_data[0])
        self.down = list(tile_data[-1])
        self.left = [r[0] for r in tile_data]
        self.right = [r[-1] for r in tile_data]

    @property
    def sides(self):
        return (
            self.up,
            self.right,
            self.down,
            self.left
        )

    def flip_h(self):
        self.left, self.right = self.right, self.left
        self.up.reverse()
        self.down.reverse()

    def flip_v(self):
        self.up, self.down = self.down, self.up
        self.left.reverse()
        self.right.reverse()

    def rotate_right(self):
        self.up, self.down, self.left, self.right = (
            reversed(self.left),
            reversed(self.right),
            self.down,
            self.up
        )

    def match(self, other):
        return any(
            (s1 == s2) or (list(reversed(s1)) == s2) for s1, s2 in itertools.product(self.sides, other.sides)
        )

    def __repr__(self):
        gap = "."*(self.tile_size-2)
        cols = "\n".join([f"{self.left[i]}{gap}{self.right[i]}" for i in range(1, self.tile_size-1)])
        return \
            f"{self.id}\n" \
            f"{''.join(self.up)}\n" \
            f"{cols}\n" \
            f"{''.join(self.down)}\n"


def matches(tiles):
    counter = defaultdict(int)
    match_tiles = filter(lambda t: t[0].id != t[1].id, itertools.product(tiles, tiles))
    for t1, t2 in match_tiles:
        counter[t1.id] += int(t1.match(t2))
    return counter


def part_1(tiles):
    counter = matches(tiles)
    return prod(id for id in counter if counter[id] == 2)


if __name__ == "__main__":
    with open("./input/advent20.txt") as f:
        tiles = list(parse_input(f))
        print(part_1(tiles))