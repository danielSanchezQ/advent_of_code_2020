from functools import reduce
from math import cos, sin, radians, ceil


def parse_input(f):
    f = (l.strip() for l in f)
    return ((l[0], int(l[1:])) for l in f)


def n(value, _, coords):
    x, y = coords
    return _, (x, y+value)


def s(value, _, coords):
    x, y = coords
    return _, (x, y-value)


def e(value, _, coords):
    x, y = coords
    return _, (x+value, y)


def w(value, _, coords):
    x, y = coords
    return _, (x-value, y)


degree_to_caard = {
    0: "N",
    90: "E",
    180: "S",
    270: "W"
}


def r(value, facing, _):
    return (facing+value) % 360, _


def l(value, facing, _):
    return (facing-value) % 360, _


def f(value, facing, coords):
    return operations[degree_to_caard[facing]](value, facing, coords)


operations = {
    "N": n,
    "S": s,
    "E": e,
    "W": w,
    "R": r,
    "L": l,
    "F": f
}


def solve(data, operations, init):
    def calc(accum, data):
        command, value = data
        res = operations[command](value, *accum)
        return res
    return reduce(calc, data, init)


def solve_1(data):
    _, coords = solve(data, operations, (90, (0, 0)))
    return coords, sum(map(abs, coords))


def rotate(angle, waypoint_coords):
    angle = radians(angle)
    x, y = waypoint_coords
    c = int(round(cos(angle)))
    s = int(round(sin(angle)))
    rx = x * c - y * s
    ry = y * c + x * s
    return rx, ry


def r_waypoint(value, ship_coords, waypoint_coords):
    # angles open counter clockwise, we need to reverse the angle
    return ship_coords, rotate(-value, waypoint_coords)


def l_waypoint(value, ship_coords, waypoint_coords):
    return ship_coords, rotate(value, waypoint_coords)


def f_to_waypoint(value, ship_coords, waypoint_coords):
    return tuple(
        x+y for x, y in zip(ship_coords, map(lambda c: c*value, waypoint_coords))
    ), waypoint_coords


def solve_2(data):
    operations = {
        "N": lambda value, ship_coords, waypoint_coords: (ship_coords, n(value, "", waypoint_coords)[1]),
        "S": lambda value, ship_coords, waypoint_coords: (ship_coords, s(value, "", waypoint_coords)[1]),
        "E": lambda value, ship_coords, waypoint_coords: (ship_coords, e(value, "", waypoint_coords)[1]),
        "W": lambda value, ship_coords, waypoint_coords: (ship_coords, w(value, "", waypoint_coords)[1]),
        "R": r_waypoint,
        "L": l_waypoint,
        "F": f_to_waypoint
    }
    ship_coords, _ = solve(data, operations, ((0, 0), (10, 1)))
    return ship_coords, sum(map(abs, ship_coords))


if __name__ == "__main__":
    with open("./input/advent12.txt") as f:
        data = list(parse_input(f))
        print(solve_1(data))
        print(solve_2(data))