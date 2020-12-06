from functools import reduce


def lower_half(lower, upper):
    return lower, lower + (upper-lower)//2


def upper_half(lower, upper):
    return lower + (upper-lower)//2, upper


operations = {
    "F": lower_half,
    "B": upper_half,
    "R": upper_half,
    "L": lower_half
}


def split_stream(stream):
    return stream[:7], stream[7:]


def seat_id(row, column):
    return row * 8 + column


def calc_row(stream):
    return max(reduce(lambda accum, letter: operations[letter](*accum), stream, (0, 127)))


def calc_column(stream):
    return max(reduce(lambda accum, letter: operations[letter](*accum), stream, (0, 7)))


def calc_ids(f):
    return (
        seat_id(calc_row(row), calc_column(column)) for row, column in map(split_stream, f)
    )


def part_1(f):
    return max(calc_ids(f))


def part_2(f):
    ids = sorted(calc_ids(f))
    m, M = ids[0], ids[-1]
    return set(range(m, M+1)).difference(set(ids)).pop()


if __name__ == "__main__":
    with open("./input/advent5.txt") as f:
        data = [l.strip() for l in f]
        print(part_1(data))
        print(part_2(data))