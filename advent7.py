import parse
from itertools import chain
from functools import lru_cache

split_tag = " bags contain "
bag_match = "{shade} {color}"
number_bags_match = "{number:d} {color}"


def clean_input_childs(el):
    return el.replace("bags", "").replace("bag", "").replace(".", "").strip()


def load_data(f):
    lines = map(lambda x: x.split(split_tag), f)
    lines = {
        head: {
            x["color"]: x["number"] for x in (
                x.named for x in (parse.parse(number_bags_match, clean_input_childs(el)) for el in tail.split(",")) if x
            )
        }
        for head, tail in lines
    }
    return lines


@lru_cache(maxsize=600)
def has_target(color, target, data):
    inner = data.inner
    childs = inner[color]
    if target in childs:
        return True
    return any(has_target(other, target, data) for other in childs)


def part1(data):
    data = HashableHack(data)
    return sum(1 for k in data.inner if has_target(k, "shiny gold", data))


@lru_cache
def calc_shiny_gold(color, data):
    inner = data.inner
    childs = inner[color]
    if not childs:
        return 0
    return sum(childs[c] + childs[c]*calc_shiny_gold(c, data) for c in childs)


def part2(data):
    data = HashableHack(data)
    return calc_shiny_gold('shiny gold', data)


class HashableHack(object):
    def __init__(self, d):
        self.inner = d

    def __hash__(self):
        return 1


if __name__ == "__main__":
    with open("./input/advent7.txt") as f:
        data = load_data(f)
    print(part1(data))
    print(part2(data))