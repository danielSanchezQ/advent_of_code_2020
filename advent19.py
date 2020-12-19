from nltk.parse import generate
from nltk.grammar import CFG
import re
import itertools


def parse_rule(rule):
    rule_id, matches = rule.split(": ")
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


def parse_rule_for_dict(rule):
    rule_id, matches = rule.rstrip().split(": ")
    if matches in {'"a"', '"b"'}:
        return rule_id, matches[1]
    matches = list(x.split() for x in matches.split(" | "))
    return rule_id, matches


def parse_rules_as_dict(rules):
    return dict(map(parse_rule_for_dict, rules))


def parse_data_as_dict(f):
    return parse_rules_as_dict(itertools.takewhile(lambda x: x not in ["", "\n"], f)), (l.rstrip() for l in f)


def rules_dict_to_regex_str(rules, index='0'):
    item = rules.get(index, index)
    if type(item) is str:
        return item
    if len(item) == 1:
        sub_re = ''.join(map(lambda i: rules_dict_to_regex_str(rules, i), item[0]))
        return f"({sub_re})"
    elif len(item) == 2:
        re_left, re_right = [''.join(map(lambda i: rules_dict_to_regex_str(rules, i), item[x])) for x in (0, 1)]
        return f"({re_left}|{re_right})"


def part_2(regex, lines):
    return sum(1 for l in lines if any(r.fullmatch(l) for r in regex))


if __name__ == "__main__":
    # with open("./input/advent19.txt") as f:
    #     rules, lines = parse_data(f)
    #     lines = list(lines)
    #     all_matches = cache_matches(rules)
    #     print(part_1(all_matches, lines))

    # part1 solved with method for part2
    with open("./input/advent19.txt") as f:
        rules, lines = parse_data_as_dict(f)
        regx = re.compile(rules_dict_to_regex_str(rules))
        print(part_2((regx, ), lines))

    with open("./input/advent19_part2.txt") as f:
        rules, lines = parse_data_as_dict(f)
        regex_str = rules_dict_to_regex_str(rules)
        print(regex_str)
        options_to_9 = [re.compile(regex_str.replace("m", str(i))) for i in range(1, 10)]
        print(part_2(options_to_9, lines))