

def load_map(path):
    with open(path) as f:
        return list(l.strip() for l in  f)


def solve(right, down, map):
    x, y = 0, 0
    limit_y = len(map)
    limit_x = len(map[0])
    counter = 0
    while y < limit_y:
        if map[y][x] == "#":
            counter += 1
        y += down
        x = (x+right) % limit_x
    return counter

solution_2_to_check = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

if __name__ == "__main__":
    from operator import mul
    from functools import reduce
    input_map = load_map("./input/advent3.txt")
    print(solve(3, 1, input_map))
    solution2 = reduce(
        mul,
        map(
            lambda x: solve(x[0], x[1], input_map),
            solution_2_to_check)
    )
    print(solution2)