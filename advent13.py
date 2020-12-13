import math

def parse_input(f):
    earliest = int(next(f))
    busses = ((i, int(x)) for i, x in enumerate(next(f).split(",")) if x != "x")
    return earliest, list(busses)


def next_from(earliest, bus):
    div = earliest // bus
    res = (bus * (div + 1)) - earliest
    return res


def part_1(earliest, busses):
    waiting, bus = min((next_from(earliest, bus), bus) for bus in busses)
    return (waiting, bus), waiting*bus


# chinese remainder theorem from rosseta code:
# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
from functools import reduce
import operator


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(operator.mul, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
######################################################


def part_2(busses):
    a, n = zip(*busses)
    # we have that t + x = 0 (mod ID), so t = -x (mod ID)
    # we need to negate the required offset for the crt to work
    a = [-e for e in a]
    return chinese_remainder(n, a)


if __name__ == "__main__":
    with open("./input/advent13.txt") as f:
        earliest, busses = parse_input(f)
        print(part_1(earliest, map(lambda x: x[1], busses)))
        print(part_2(busses))
