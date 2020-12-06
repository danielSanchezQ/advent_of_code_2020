from functools import reduce


def load_data(f):
    groups = f.read().split("\n\n")
    subgroups = ([set(x) for x in g.split("\n")] for g in groups)
    return subgroups


def merge_answers(group_answers, operation):
    return reduce(operation, group_answers)


def part_1(data):
    return sum(len(answers) for answers in map(lambda x: merge_answers(x, set.union), data))


def part_2(data):
    return sum(len(answers) for answers in map(lambda x: merge_answers(x, set.intersection), data))


if __name__ == "__main__":
    with open("./input/advent6.txt") as f:
        data = list(load_data(f))
        print(part_1(data))
        print(part_2(data))