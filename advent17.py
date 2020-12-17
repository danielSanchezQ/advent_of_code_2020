from collections import defaultdict
import itertools


Active = "#"
Inactive = "."


def grid(size, def_value):
    if size <= 1:
        return defaultdict(lambda: def_value)
    return defaultdict(lambda: grid(size-1, def_value))


class CubeState(object):
    __slots__ = ["grid", "coords", "dimensions", "range_to_check"]

    def __init__(self, coords, dimensions, range_to_check):
        self.coords = coords
        self.range_to_check = range_to_check
        self.dimensions = dimensions
        self.grid = grid(dimensions, Inactive)
        self._load_grid()

    def coords_to_check(self):
        m, M = self.range_to_check
        return itertools.product(range(m-1, M+1), repeat=self.dimensions)

    def get(self, coords):
        dimension = self.grid
        for coord in coords[:-1]:
            dimension = dimension[coord]
        return dimension[coords[-1]]

    def set(self, coords, value):
        dimension = self.grid
        for coord in coords[:-1]:
            dimension = dimension[coord]
        dimension[coords[-1]] = value

    def _load_grid(self):
        for coord in self.coords:
            self.set(coord, Active)


def parse_data(f):
    z = 0
    return [(x, y, z) for x, l in enumerate(f) for y, c in enumerate(l.rstrip()) if c == Active]


def surround_coords(dimensions):
    return filter(lambda x: x != tuple([0]*dimensions), itertools.product((0, 1, -1), repeat=dimensions))


surround_cache = {i: list(surround_coords(i)) for i in [3, 4]}


def add_coords(c1, c2):
    return tuple(x+y for x, y in zip(c1, c2))


def neighbors(coords):
    return (add_coords(c1, c2) for c1, c2 in zip(itertools.repeat(coords), surround_cache[len(coords)]))


def get_active_state_for_coords(coords, state):
    if sum(1 for coord in neighbors(coords) if state.get(coord) == Active) in {2, 3}:
        return Active
    return Inactive


def get_inactive_state_for_coords(coords, state):
    if sum(1 for coord in neighbors(coords) if state.get(coord) == Active) == 3:
        return Active
    return Inactive


def iter_one(operations, state):
    new_active = [
        coords for coords in state.coords_to_check() if operations[state.get(coords)](coords, state) == Active
    ]
    (m, M) = state.range_to_check
    return CubeState(new_active, state.dimensions, (m-1, M+1))


def solve(state, n):
    operations = {
        Active: get_active_state_for_coords,
        Inactive: get_inactive_state_for_coords,
    }
    for i in range(n):
        state = iter_one(operations, state)
    return len(state.coords)


if __name__ == "__main__":
    with open("./input/advent17.txt") as f:
        initial_ranges = (0, 8)
        data = parse_data(f)
        initial_state = CubeState(data, 3, initial_ranges)
        print(solve(initial_state, 6))
        initial_state = CubeState(map(lambda x: (*x, 0), data), 4, initial_ranges)
        print(solve(initial_state, 6))
