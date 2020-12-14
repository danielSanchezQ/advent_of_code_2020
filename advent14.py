from parse import parse
from functools import reduce, lru_cache
import itertools

parse_mask = "mask = {mask}"
parse_mem = "mem[{address:d}] = {value:d}"


def parse_one(line):
    if parsed := parse(parse_mask, line):
        return "mask", parsed["mask"]
    elif parsed := parse(parse_mem, line):
        return "mem", parsed["address"], parsed["value"]


def parse_all(stream):
    return map(parse_one, stream)


def to_binary(n):
    return f"{n:0>36b}"


class State(object):
    __slots__ = ["mem", "mask"]

    def __init__(self):
        self.mask = None
        self.mem = {}

    def __setitem__(self, key, value):
        self.mem.__setitem__(key, value)

    def __getitem__(self, item):
        self.mem.__getitem__(item)


def mask_bit(b1, b2):
    return b2 if b1 == "X" else b1


def str_mask_value(mask_bit, mask, value):
    return "".join(mask_bit(b1, b2) for b1, b2 in zip(mask, value))


def mask_value(mask_bit, mask, value):
    return int(str_mask_value(mask_bit, mask, value), 2)


def execute_mask(state, value):
    state.mask = value


def execute_mem(state, address, value):
    state[address] = mask_value(mask_bit, state.mask, to_binary(value))


def solve(operations, stream):
    def reducer(state, data):
        command, *values = data
        operations[command](state, *values)
        return state

    final_state = reduce(reducer, stream, State())
    return sum(final_state.mem.values())


def part_1(stream):
    operations = {
        "mask": execute_mask,
        "mem": execute_mem
    }
    return solve(operations, stream)


def mask_bit2(b1, b2):
    return b1 if b1 in {"1", "X"} else b2


def combinations_with_size(size):
    yield from itertools.product("01", repeat=size)


def iter_mask(mask):
    indexes = set(i for i, e in enumerate(mask) if e == "X")
    combinations = combinations_with_size(len(indexes))
    for combination in combinations:
        subs = iter(combination)
        sub_mask = "".join(next(subs) if i in indexes else mask[i] for i in range(len(mask)))
        yield sub_mask


def execute_mem2(state, address, value):
    address_mask = str_mask_value(mask_bit2, state.mask, to_binary(address))
    for mask in iter_mask(address_mask):
        state[int(mask, 2)] = value


def part_2(stream):
    operations = {
        "mask": execute_mask,
        "mem": execute_mem2
    }
    return solve(operations, stream)


if __name__ == "__main__":
    with open("./input/advent14.txt") as f:
        data = list(parse_all(f))
        print(part_1(data))
        print(part_2(data))