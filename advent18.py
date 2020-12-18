# override operator precedence, we just need to wrap incoming values
class OverloadedValue(object):
    def __init__(self, value):
        self.value = int(value)

    def __mul__(self, other):
        return OverloadedValue(self.value * other.value)

    def __add__(self, other):
        return OverloadedValue(self.value + other.value)

    def __repr__(self):
        return f"OverloadedValue({self.value})"

    __sub__ = __mul__
    __pow__ = __add__


def replace_line(l):
    return l.rstrip().replace("(", "( ").replace(")", " )").replace("*", "-")


def parse_data(l: str):
    return " ".join(
        str(OverloadedValue(int(c))) if c.isdigit() else c for c in replace_line(l).split()
    )


def load_data(f):
    return map(parse_data, f)


def solve(f):
    return sum(eval(l).value for l in f)


if __name__ == "__main__":
    with open("./input/advent18.txt") as f:
        data = list(load_data(f))
        # part 1
        print(solve(data))
        # part 2
        print(solve((l.replace("+", "**") for l in data)))