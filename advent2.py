import parse


def parse_data(data):
    fmt_str = "{}-{} {}: {}"
    matches = parse.parse(fmt_str, data)
    return int(matches[0]), int(matches[1]), matches[2], matches[3]


def validate1(l, L, letter, pwd):
    return l <= pwd.count(letter) <= L


def validate2(p1, p2, letter, pwd):
    i1, i2 = p1-1, p2-1
    return (pwd[i1] == letter) ^ (pwd[i2] == letter)


def pipe(f, validate_f):
    return sum(1 for data in f if validate_f(*parse_data(data)))


def sol1(f):
    return pipe(f, validate1)


def sol2(f):
    return pipe(f, validate2)


if __name__ == "__main__":
    from itertools import tee
    with open("./input/advent2.txt") as f:
        f1, f2 = tee(f)
        print(sol1(f1))
        print(sol2(f2))