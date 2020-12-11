import itertools
from copy import copy


class Layout(object):
    __slots__ = ["row_size", "column_size", "layout"]

    def __init__(self, row_size, column_size, layout):
        self.layout = layout
        self.row_size = row_size
        self.column_size = column_size

    def _calc_position(self, row, column):
        assert row < self.row_size
        assert column < self.column_size
        position = row * self.column_size + column
        return position

    def get(self, row, column):
        position = self._calc_position(row, column)
        return self.layout[position]

    def set(self, row, column, value):
        position = self._calc_position(row, column)
        self.layout[position] = value

    def get_adjacent_seats_positions(self, row, column):
        return (
            (r, c) for x, y in itertools.product((1, 0, -1), (1, 0, -1)) if
            (0 <= (r := row+x) < self.row_size) and
            (0 <= (c := column+y) < self.column_size) and
            (r, c) != (row, column)
        )

    def count(self, value):
        return sum(1 for e in self.layout if e == value)

    def __getitem__(self, row):
        # this is probably a bad idea since it adds a lot of overhead
        # but hey, its nice to have :D
        class _InnerGetter(object):

            def __init__(self, layout):
                self.layout = layout

            def __getitem__(self, column):
                return self.layout.get(row, column)

            def __setitem__(self, column, value):
                return self.layout.set(row, column, value)
        return _InnerGetter(self)

    def __eq__(self, other):
        return (
            self.row_size == other.row_size and
            self.column_size == other.column_size and
            self.layout == other.layout
        )

    def __copy__(self):
        return Layout(self.row_size, self.column_size, self.layout.copy())

    def __str__(self):
        it = iter(self.layout)
        return "\n".join(
            "".join(next(it) for _ in range(self.column_size)) for _ in range(self.row_size)
        )


def load_layout(f):
    line1 = next(f).strip()
    column_size = len(line1)
    layout = list(line1)
    row_size = 1
    for e in f:
        layout.extend(e.strip())
        row_size += 1
    return Layout(row_size, column_size, layout)


Empty = 'L'
Floor = '.'
Occupied = '#'


def rule1(row, column, old_layout, layout):
    # If a seat is empty (L) and there are no occupied seats adjacent to it,
    # the seat becomes occupied
    adjacent = old_layout.get_adjacent_seats_positions(row, column)
    if all(old_layout[r][c] != Occupied for r, c in adjacent):
        layout[row][column] = Occupied


def rule2(row, column, old_layout, layout):
    # If a seat is occupied (#) and four or more seats
    # adjacent to it are also occupied, the seat becomes empty.
    if sum(1 for r, c in old_layout.get_adjacent_seats_positions(row, column) if old_layout[r][c] == Occupied) >= 4:
        layout[row][column] = Empty


def iter_one(rules, old_layout, layout):
    for r, c in itertools.product(range(layout.row_size), range(layout.column_size)):
        item = old_layout[r][c]
        rules[item](r, c, old_layout, layout)


def solve(rules, layout):
    iteration = 0
    while True:
        old_layout = copy(layout)
        iter_one(rules, old_layout, layout)
        if layout == old_layout:
            return layout.count(Occupied)
        iteration += 1


def solve_1(layout):
    rules = {
        Empty: rule1,
        Occupied: rule2,
        Floor: lambda *_: None
    }
    return solve(rules, layout)


def seat_view(row, column, old_layout):
    seats = {Empty, Occupied}
    w = next((seat for c in range(column-1, -1, -1) if (seat := old_layout[row][c]) in seats), None)
    e = next((seat for c in range(column+1, layout.column_size) if (seat := old_layout[row][c]) in seats), None)
    n = next((seat for r in range(row-1, -1, -1) if (seat := old_layout[r][column]) in seats), None)
    s = next((seat for r in range(row+1, layout.row_size) if (seat := old_layout[r][column]) in seats), None)
    nw = next((seat for i in range(1, min(row, column)+1) if (seat := old_layout[row-i][column-i]) in seats), None)
    ne = next((seat for i in range(1, min(row+1, layout.column_size - column)) if (seat := old_layout[row-i][column+i]) in seats), None)
    sw = next((seat for i in range(1, min(layout.row_size - row, column+1)) if (seat := old_layout[row+i][column-i]) in seats), None)
    se = next((seat for i in range(1, min(layout.row_size - row, layout.column_size - column)) if (seat := old_layout[row+i][column+i]) in seats), None)
    return n, s, e, w, ne, nw, se, sw


def rule1_prime(row, column, old_layout, layout):
    view = seat_view(row, column, old_layout)
    if all(e != Occupied for e in view):
        layout[row][column] = Occupied


def rule2_prime(row, column, old_layout, layout):
    view = seat_view(row, column, old_layout)
    if sum(1 for e in view if e == Occupied) >= 5:
        layout[row][column] = Empty


def solve_2(layout):
    rules = {
        Empty: rule1_prime,
        Occupied: rule2_prime,
        Floor: lambda *_: None
    }
    return solve(rules, layout)


if __name__ == "__main__":
    with open("./input/advent11.txt") as f:
        layout = load_layout(f)
        print("Result 1: ", solve_1(copy(layout)))
        print("Result 2", solve_2(layout))