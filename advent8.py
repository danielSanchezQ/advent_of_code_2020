def parse_program(f):
    def parse_line(l):
        cmd, value = l.split()
        return cmd, int(value)
    return list(parse_line(l) for l in f)


class State(object):
    __slots__ = ["accum", "index", "program_size", "visited"]

    def __init__(self, program_size):
        self.accum = 0
        self.index = 0
        self.program_size = program_size
        self.visited = set()


def acc(state: State, value: int):
    state.accum += value
    inc(state)


def jmp(state: State, value: int):
    state.visited.add(state.index)
    new_index = (state.index + value) % state.program_size
    state.index = new_index


def inc(state: State, *_):
    state.visited.add(state.index)
    state.index += 1

nop = inc

operations = {
    "acc": acc,
    "jmp": jmp,
    "nop": nop,
}


def run(state, program):
    while state.index not in state.visited:
        if len(state.visited) == len(program):
            return state.accum
        cmd, value = program[state.index]
        operations[cmd](state, value)
    return state.accum


def run2(state, program):
    while state.index not in state.visited:
        cmd, value = program[state.index]
        operations[cmd](state, value)
        if state.index == (len(program)-1):
            return state.accum


def program_gen(program):
    original = program.copy()
    for i, (cmd, value) in enumerate(program):
        if cmd == "nop":
            cmd = "jmp"
        elif cmd == "jmp":
            cmd = "nop"
        else:
            continue
        ret = original.copy()
        ret[i] = (cmd, value)
        yield ret


def run2_all(program):
    for p in program_gen(program):
        state = State(len(program))
        res = run2(state, p)
        if res:
            return res


if __name__ == "__main__":
    with open("./input/advent8.txt") as f:
        program = parse_program(f)
        state = State(len(program))
        result = run(state, program)
        print(result)
        result = run2_all(program)
        print(result)