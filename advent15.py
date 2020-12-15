from collections import defaultdict


initial_data = [1,20,11,6,12,0]


class State(object):
    __slots__ = ["counter", "i", "last"]

    def __init__(self, input):
        self.counter = defaultdict(int)
        self.counter.update({k: c for c, k in enumerate(input[:-1], 1)})
        self.i = len(input)
        self.last = input[-1]

    def iter_one(self):
        self.i += 1
        if self.last not in self.counter:
            self.counter[self.last] = self.i - 1
            self.last = 0
        else:
            prev_last_turn = self.counter[self.last]
            self.counter[self.last] = self.i - 1
            self.last = self.i - prev_last_turn - 1


def solve(n, state):
    while state.i < n:
        state.iter_one()
    return state.last


if __name__ == "__main__":
    state = State(initial_data)
    print(solve(2020, state))
    print(solve(30000000, state))
