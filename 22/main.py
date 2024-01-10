import sys
from typing import List, Dict

from brick import Brick, print_bricks_3d, print_bricks_z
from shared import input

bricks_to_test_cache: Dict[int, set[Brick]] = {}


# 659 is too high
# 428 is right
#
# 25992 is too low
# 36885 is too high
# 36884 is too high
# 35654 is right
def main(filename: str):
    lines = input.readfile(filename)
    # print(lines)

    bricks = []

    label = 'A01'
    # label = '0'

    for line in lines:
        start, end = line.split('~')

        x1, y1, z1 = start.split(',')
        x2, y2, z2 = end.split(',')

        if z2 < z1:
            x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1

        brick = Brick((int(x1), int(y1), int(z1)), (int(x2), int(y2), int(z2)), label)

        if brick.z_max not in bricks_to_test_cache.keys():
            bricks_to_test_cache[brick.z_max] = set()

        bricks_to_test_cache[brick.z_max].add(brick)

        bricks.append(brick)
        # label = chr(ord(label) + 1)
        # label = (chr(ord(label[0]) + 1) if label[0] != 'Z' else 'A') + f"{('00' if label[0] != 'Z' else str(int(label[1]) + 1)):02}"

        letter, number = label[0], int(label[1:])

        if number == 99:
            letter = chr(ord(letter) + 1)
            number = 1
        else:
            number +=1

        label = f'{letter}{number:02}'

    bricks.sort(key=lambda brick: brick.z_min)

    # print_bricks(bricks)
    print(f'Total bricks: {len(bricks)}')
    # print_bricks_3d(bricks)
    print_bricks_z(bricks, 1)
    # print_bricks_z(bricks, 2)
    # print_bricks_z(bricks, 3)

    settle_bricks(bricks)

    # print()
    # print_bricks(bricks)
    # print_bricks_3d(bricks)
    # print_bricks_z(bricks, 1)

    print()
    print(f'Supported: {sum([1 for brick in bricks if brick.is_supported])}/{len(bricks)}')
    print(f'Safe to disintegrate: {sum([1 for brick in bricks if brick.safe_to_disintegrate])}')

    total_will_fall = 0

    for brick in bricks:
        will_fall = brick.will_fall_if_disintegrated
        # print(f'{brick.label}: {will_fall} will fall')
        total_will_fall += will_fall

    # print()
    print(f'Total bricks that will fall: {total_will_fall}')


def clone_bricks(bricks):
    new_bricks = []

    for brick in bricks:
        new_brick = Brick(brick.start, brick.end)
        new_brick.label = brick.label
        new_brick.supports = brick.supports
        new_brick.is_supported = brick.is_supported
        new_bricks.append(new_brick)

    return new_brick


def lower_brick(brick, bricks):
    # print(f'Lowering brick {brick}')

    while True:
        if brick.is_supported:
            # print('Already supported')
            return

        bricks_to_test = bricks_to_test_cache[brick.z_min - 1] if brick.z_min - 1 in bricks_to_test_cache.keys() else set()
        brick.move_down()

        intersects = [b for b in bricks_to_test if brick.intersects(b)]

        if intersects:
            # print(f'Intersections found: {intersects}')
            brick.is_supported_by += intersects
            brick.move_up()

            for b in intersects:
                b.supports.append(brick)

            return

        bricks_to_test_cache[brick.z_max + 1].remove(brick)

        if brick.z_max not in bricks_to_test_cache.keys():
            bricks_to_test_cache[brick.z_max] = set()

        bricks_to_test_cache[brick.z_max].add(brick)


def print_bricks(bricks):
    for brick in reversed(bricks):
        print(brick, brick.dimensions, brick.volume)

    print()


def settle_bricks(bricks: List[Brick]):
    highest_supported = 0

    while highest_supported < len(bricks):
        for brick in bricks[highest_supported:]:
            lower_brick(brick, bricks)
            # print(f'Brick is now: {brick}')

            if brick.is_supported:
                highest_supported += 1
                print(f'Highest supported now: {highest_supported}')


if __name__ == '__main__':
    main(sys.argv[1])
