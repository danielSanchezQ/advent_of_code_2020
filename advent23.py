import itertools
from math import prod


initial_state = [
    6, 2, 4, 3, 9, 7, 1, 5, 8
]


def take(it, n):
    yield from (next(it) for _ in range(n))


def drop(it, n):
    for _ in range(n):
        next(it)


def select_next(current: int, state: list):
    while current > 0:
        current -= 1
        try:
            return state.index(current)
        except ValueError:
            continue
    return state.index(max(state))


def move_one(current_cup_index: int, state: list):
    current_cup = state[current_cup_index]
    next_3 = [state[(i+current_cup_index+1) % len(state)] for i in range(3)]
    for e in next_3:
        state.remove(e)
    destination_cup = select_next(current_cup, state)
    for e in reversed(next_3):
        state.insert(destination_cup+1, e)
    return (state.index(current_cup) + 1) % len(state)


def state_to_str(state: list):
    index_1 = state.index(1)
    seq = itertools.cycle(state)
    drop(seq, index_1+1)
    return "".join(str(i) for i in take(seq, len(state)-1))


def solve(state, n):
    current_cup_index = 0
    for _ in range(n):
        current_cup_index = move_one(current_cup_index, state)
    return state


def pick_next(from_label, state, n):
    for _ in range(n):
        ret = state[from_label]
        yield ret
        from_label = ret


def move_one2(current_label, state):
    next_3 = list(pick_next(current_label, state, 3))
    state[current_label] = state[next_3[-1]]
    destination_label = select_next_label(current_label, state, next_3)
    insert_on_destination(destination_label, next_3, state)
    return next(pick_next(current_label, state, 1))


def insert_on_destination(destination_label, next_3, state):
    latest = state[destination_label]
    state[destination_label] = next_3[0]
    state[next_3[-1]] = latest


def select_next_label(current_label, state, picked):
    picked = set(picked)
    while current_label > 0:
        current_label -= 1
        if current_label in state and current_label not in picked:
            return current_label
    return max(set(state.keys()).difference(picked))


def solve_2(state, n):
    circular = dict(zip(state, itertools.islice(state, 1, len(state))))
    circular[state[-1]] = state[0]
    current_label = state[0]
    for _ in range(n):
        current_label = move_one2(current_label, circular)
    return circular


def calc_part_2(final_state):
    return prod(pick_next(1, final_state, 2))


if __name__ == "__main__":
    # part 1
    print(state_to_str(solve(initial_state.copy(), 100)))
    # part 1 with method 2
    print("".join(str(i) for i in (pick_next(1, solve_2(initial_state.copy(), 100), len(initial_state) - 1))))
    # part 2
    state2 = initial_state + list(range(10, 1000001))
    print(calc_part_2(solve_2(state2, 10000000)))