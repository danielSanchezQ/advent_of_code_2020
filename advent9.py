import itertools


def take(it, n):
    yield from (next(it) for _ in range(n))


def extend_one(l, new_value):
    l.pop(0)
    l.append(new_value)


def check_sum(l, value):
    return any((a+b) == value for a, b in itertools.product(l, l) if a != b)


def solve_1(f):
    f = map(int, f)
    preamble = list(take(f, 25))
    while True:
        new_value = next(f)
        if not check_sum(preamble, new_value):
            return new_value
        extend_one(preamble, new_value)


# sliding windows from https://stackoverflow.com/a/6822773/1695172
from itertools import islice


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result
########################################################################


def all_windows(seq):
    yield from itertools.chain.from_iterable(window(seq, size) for size in range(2, len(seq)))


def calc_value_from_window(seq):
    return min(seq) + max(seq)


def solve_2(f, n):
    cache_nums = list(map(int, f))
    return next(calc_value_from_window(w) for w in all_windows(cache_nums) if sum(w) == n)


if __name__ == "__main__":
    with open("./input/advent9.txt") as f:
        found_n = solve_1(f)
        print(found_n)

    with open("./input/advent9.txt") as f:
        crack_n = solve_2(f, found_n)
        print(crack_n)
