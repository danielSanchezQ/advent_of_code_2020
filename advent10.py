from collections import defaultdict
import itertools
from functools import reduce
import operator


def parse_input(f):
    return sorted(list(map(int, f)))


def solution_1(data):
    diffs = defaultdict(int)
    diffs[data[0]] += 1
    for a, b in zip(data, data[1:]):
        diffs[b-a] += 1
    diffs[3] += 1
    return diffs


# valid permutation for subgroups of [1], [1, 1], [1, 1, 1], [1, 1, 1, 1] differences
perms = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
}


def solution_2(data):
    diffs = (b-a for a, b in zip(data, data[1:]))
    grouped = (list(v) for k, v in itertools.groupby(diffs) if k == 1)
    res = reduce(operator.mul, map(lambda x: perms[len(x)], grouped))
    return res


if __name__ == "__main__":
    with open("./input/advent10.txt") as f:
        data = parse_input(f)
        solved_diffs = solution_1(data)
        print(solved_diffs[1]*solved_diffs[3])
        print(solution_2([0, *data, data[-1]+3]))




