import itertools

base_n = 20_201_227


def transform(subject_number, loop_size):
    return pow(subject_number, loop_size, mod=base_n)


def reverse_loop(subject_number, pks):
    value = 1
    res = {}
    for loop_size in itertools.count(1):
        value = (value * subject_number) % base_n
        if value in pks:
            res[value] = loop_size
        if len(pks) == len(res):
            return res


def solve_1(keys, subject_number):
    card_pk, door_pk = keys
    loop_sizes = reverse_loop(subject_number, set(keys))
    card_ek = transform(door_pk, loop_sizes[card_pk])
    door_ek = transform(card_pk, loop_sizes[door_pk])
    assert card_ek == door_ek
    return card_ek


if __name__ == "__main__":
    keys = [
        6_270_530,
        14_540_258
    ]
    subject_number = 7
    print(solve_1(keys, subject_number))