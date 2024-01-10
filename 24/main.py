import sys
import time

from enum import Enum
from shared import input
from sympy import *


class CrossingStatus(Enum):
    PARALLEL = 0
    PAST_A = 1
    PAST_B = 2
    INSIDE = 3
    OUTSIDE = 4
    UNKNOWN = 5


class HailStone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return f'<{self.position} @ {self.velocity}>'


# 11246 is right
#
# 716599937560103 is right
def main(filename: str):
    lines = input.readfile(filename)
    hail_stones = process_lines(lines)
    crossing_count = 0
    test_area = (7, 7), (27, 27)
    # test_area = (200000000000000, 200000000000000), (400000000000000, 400000000000000)
    total_stones = len(hail_stones)
    start_time = None
    total_time = None
    next_time = None

    h0, h1, h2 = hail_stones[0:3]
    print('Calculating intercept course with hail stones:')

    for h in [h0, h1, h2]:
        print(h)

    print()

    P, V = calculate_intercept_vector(h0, h1, h2)

    print(f'Intercept vector calculated: {P} @ {V}')
    print(f'Answer: {sum(P)}')

    # for i, hail_stone1 in enumerate(hail_stones):
    #     if start_time:
    #         total_time = time.time() - start_time
    #         time_per = total_time / (total_stones - (i - 1))
    #         next_time = time_per * ((total_stones - i) * (total_stones - i + 1)) / 2
    #
    #     print(f'Computing intersections for hailstone {i + 1} ({((total_stones - i) * (total_stones - i + 1)) // 2} remaining, {crossing_count} found, time this round: {total_time}s, {next_time}s left):')
    #     start_time = time.time()
    #     for j, hail_stone2 in enumerate(hail_stones[i + 1:]):
    #         # print(f'Hailstone A: {hail_stone1}')
    #         # print(f'Hailstone B: {hail_stone2}')
    #         status, crossing_point = will_cross(hail_stone1, hail_stone2, test_area)
    #
    #         match status:
    #             case CrossingStatus.INSIDE:
    #                 crossing_count += 1
    #
    #         # print()
    # print()
    # print(f'Hail stone crossing count: {crossing_count}')


def calculate_intercept_vector(h0: HailStone, h1: HailStone, h2: HailStone) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    p0 = Matrix(h0.position)
    v0 = Matrix(h0.velocity)

    p1 = Matrix(h1.position)
    v1 = Matrix(h1.velocity)

    p2 = Matrix(h2.position)
    v2 = Matrix(h2.velocity)

    C_p = Matrix([[(v0 - v1).cross(p0 - p1).transpose()], [(v0 - v2).cross(p0 - p2).transpose()], [(v1 - v2).cross(p1 - p2).transpose()]])
    C_v = Matrix([[(p0 - p1).cross(v0 - v1).transpose()], [(p0 - p2).cross(v0 - v2).transpose()], [(p1 - p2).cross(v1 - v2).transpose()]])

    D_p = Matrix([[(v0 - v1).dot(p0.cross(p1)).transpose()], [(v0 - v2).dot(p0.cross(p2)).transpose()], [(v1 - v2).dot(p1.cross(p2)).transpose()]])
    D_v = Matrix([[(p0 - p1).dot(v0.cross(v1)).transpose()], [(p0 - p2).dot(v0.cross(v2)).transpose()], [(p1 - p2).dot(v1.cross(v2)).transpose()]])

    P = Matrix.inv(C_p) * D_p
    V = Matrix.inv(C_v) * D_v

    return tuple(P), tuple(V)


def will_cross(hail_stone1: HailStone, hail_stone2: HailStone, test_area: tuple[tuple[int, int], tuple[int, int]]):
    x, y, z, t, t1, t2 = symbols('x y z t t1 t2')

    x_a = hail_stone1.position[0] + hail_stone1.velocity[0] * t1
    y_a = hail_stone1.position[1] + hail_stone1.velocity[1] * t1
    z_a = hail_stone1.position[2] + hail_stone1.velocity[2] * t1

    x_b = hail_stone2.position[0] + hail_stone2.velocity[0] * t2
    y_b = hail_stone2.position[1] + hail_stone2.velocity[1] * t2
    z_b = hail_stone2.position[2] + hail_stone2.velocity[2] * t2

    sols = list(linsolve([x_a - x_b, y_a - y_b, z_a - z_b], (t1, t2)))

    if not sols:
        return CrossingStatus.PARALLEL, None

    t_a, t_b = sols[0]

    if t_a < 0:
        return CrossingStatus.PAST_A, None

    if t_b < 0:
        return CrossingStatus.PAST_B, None

    x_cross = x_a.subs(t1, t_a).round(3)
    y_cross = y_a.subs(t1, t_a).round(3)

    crossing_point = (x_cross, y_cross)

    (x_test_min, y_test_min), (x_test_max, y_test_max) = test_area

    if x_test_min <= x_cross <= x_test_max and y_test_min <= y_cross <= y_test_max:
        return CrossingStatus.INSIDE, crossing_point
    else:
        return CrossingStatus.OUTSIDE, crossing_point

    return CrossingStatus.UNKNOWN, None


def process_lines(lines):
    hail_stones = []

    for line in lines:
        position, velocity = line.split(' @ ')
        x_p, y_p, z_p = position.split(', ')
        x_v, y_v, z_v = velocity.split(', ')
        hail_stones.append(HailStone((int(x_p), int(y_p), int(z_p)), (int(x_v), int(y_v), int(z_v))))

    return hail_stones


if __name__ == '__main__':
    main(sys.argv[1])