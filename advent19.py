from nltk.parse import generate
from nltk.grammar import CFG

import itertools


def parse_rule(rule):
    rule_id, matches = rule.split(": ")
    rule_id = int(rule_id)
    matches = matches.rstrip()
    if matches in {'"a"', '"b"'}:
        return f"{rule_id} -> '{matches[1]}'"
    return f"{rule_id} -> {matches}"


def parse_rules(rules):
    return "\n".join(parse_rule(rule) for rule in rules)

def parse_data(f):
    return parse_rules(itertools.takewhile(lambda x: x not in ["", "\n"], f)), (l.rstrip() for l in f)


def generate_from_rules(rules):
    grammar = CFG.fromstring(rules)
    yield from generate.generate(grammar)


def cache_matches(rules):
    return set("".join(x) for x in generate_from_rules(rules))


def part_1(matches, lines):
    return sum(1 for l in lines if l in matches)


if __name__ == "__main__":
    with open("./input/advent19.txt") as f:
        rules, lines = parse_data(f)
        all_matches = cache_matches(rules)
        print(part_1(all_matches, lines))
