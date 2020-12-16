import parse
import itertools
from functools import reduce
import operator


parse_range = "{:d}-{:d}"


def parse_rule(l):
    name, data = l.split(": ")
    ranges = parse.findall(parse_range, data)
    ranges = (tuple(map(int, r)) for r in ranges)
    return name, [range(m, M+1) for m, M in ranges]


def parse_ticket(l):
    l = l.rstrip().split(",")
    return list(map(int, l))


def parse_data(f):
    rules = dict(parse_rule(l) for l in itertools.takewhile(lambda x: x != "\n", f))
    # skip 'your ticket'
    next(f)
    our_ticket = parse_ticket(next(f))
    # skip new line and 'nearby tickets'
    for _ in range(2):
        next(f)
    nearby_tickets = list(map(parse_ticket, f))
    return rules, our_ticket, nearby_tickets


def is_invalid(rules, data):
    ranges = list(itertools.chain.from_iterable(rules.values()))
    return next((n for n in data if not any(n in range for range in ranges)), False)


def part_1(rules, tickets):
    return sum(invalid_num for ticket in tickets if (invalid_num := is_invalid(rules, ticket)))


def all_posible_rules(rules, tickets):
    for i in range(len(rules)):
        yield [
            rule for rule, ranges in rules.items() if all(any(t[i] in r for r in ranges) for t in tickets)
        ]


def reduce_rules(posbile_rules):
    ordered_rules = sorted(enumerate(posbile_rules), key=lambda x: len(x[1]))
    positions = [None] * 20
    visited = set()
    for i, rule in ordered_rules:
        valid_rule = next(iter(set(rule)-visited), None)
        positions[i] = valid_rule
        visited.add(valid_rule)
    return positions


def part_2(rules, my_ticket, tickets):
    tickets = list(filter(lambda x: is_invalid(rules, x) is False, tickets))
    tickets.append(my_ticket)
    possible_rules = all_posible_rules(rules, tickets)
    ordered_rules = reduce_rules(possible_rules)
    my_ticket_values = (
        value for rule_name, value in zip(ordered_rules, my_ticket) if rule_name.startswith("departure")
    )
    return reduce(operator.mul, my_ticket_values)


if __name__ == "__main__":
    with open("./input/advent16.txt") as f:
        rules, my_ticket, tickets = parse_data(f)
        print(part_1(rules, tickets))
        print(part_2(rules, my_ticket, tickets))
