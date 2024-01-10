from typing import Tuple, Optional, List


class Brick:
    def __init__(self, start: Tuple[int, int, int], end: Tuple[int, int, int], label: str):
        self.start = start
        self.end = end
        self.label = label
        self.is_supported_by: List[Brick] = []
        self.supports: List[Brick] = []

    def __repr__(self):
        return f'{self.label}: {self.start}~{self.end} Supported by: {[b.label for b in self.is_supported_by]}, Supports: {[b.label for b in self.supports]}, Safe: {self.safe_to_disintegrate}'

    @property
    def is_supported(self):
        return self.z_min == 1 or bool(self.is_supported_by)

    @property
    def z_min(self):
        return min(self.start[2], self.end[2])

    @property
    def z_max(self):
        return max(self.start[2], self.end[2])

    @property
    def y_min(self):
        return min(self.start[1], self.end[1])

    @property
    def y_max(self):
        return max(self.start[1], self.end[1])

    @property
    def x_min(self):
        return min(self.start[0], self.end[0])

    @property
    def x_max(self):
        return max(self.start[0], self.end[0])

    @property
    def dimensions(self) -> Tuple[int, int, int]:
        return (
            abs(self.start[0] - self.end[0]) + 1,
            abs(self.start[1] - self.end[1]) + 1,
            abs(self.start[2] - self.end[2]) + 1,
        )

    @property
    def volume(self) -> int:
        dimensions = self.dimensions

        return dimensions[0] * dimensions[1] * dimensions[2]

    @property
    def safe_to_disintegrate(self) -> bool:
        for brick in self.supports:
            if len(brick.is_supported_by) < 2:
                return False

        return True

    @property
    def will_fall_if_disintegrated(self) -> int:
        will_fall = set([self])
        am_supporting = self.supports

        while am_supporting:
            next_round = set()

            for brick in am_supporting:
                other_supports = [b for b in brick.is_supported_by if b not in will_fall]

                if not other_supports:
                    will_fall.add(brick)

                    for b in brick.supports:
                        next_round.add(b)

            am_supporting = next_round

        return len(will_fall) - 1


    def move_up(self):
        self.start = self.start[0], self.start[1], self.start[2] + 1
        self.end = self.end[0], self.end[1], self.end[2] + 1

    def move_down(self):
        self.start = self.start[0], self.start[1], self.start[2] - 1
        self.end = self.end[0], self.end[1], self.end[2] - 1

    def crosses_x(self, x: int):
        return self.x_min <= x <= self.x_max

    def crosses_y(self, y: int):
        return self.y_min <= y <= self.y_max

    def crosses_z(self, z: int):
        return self.z_min <= z <= self.z_max

    def intersects(self, block: 'Brick') -> Optional[Tuple[int, int, int]]:
        for z in range(self.z_min, self.z_max + 1):
            if block.crosses_z(z):
                for y in range(self.y_min, self.y_max + 1):
                    if block.crosses_y(y):
                        for x in range(self.x_min, self.x_max + 1):
                            if block.crosses_x(x):
                                return x, y, z

        return None


def print_bricks_3d(bricks):
    x_max = max([brick.x_max for brick in bricks])
    y_max = max([brick.y_max for brick in bricks])
    z_max = max([brick.z_max for brick in bricks])

    line = ' x' + ' ' * (((x_max + 3) * 5) - 3) + 'y'
    print(line)

    line = ''

    for i in range(x_max + 1):
        line += f' {i}   '

    line += ' ' * 8

    for i in range(y_max + 1):
        line += f' {i}   '

    print(line)

    for z in range(z_max, 0, -1):
        line = ''

        for i in range(x_max + 1):
            intersecting: List[Brick]
            intersecting = [brick for brick in bricks if brick.crosses_z(z) and brick.crosses_x(i)]

            if intersecting:
                intersecting.sort(key=lambda brick: brick.x_min)

                if len(intersecting) > 1:
                    line += ' ??? '
                else:
                    line += f' {intersecting[0].label} '
            else:
                line += ' ... '

        line += f' {z:03}' + ' ' * 4

        for i in range(y_max + 1):
            intersecting: List[Brick]
            intersecting = [brick for brick in bricks if brick.crosses_z(z) and brick.crosses_y(i)]

            if intersecting:
                intersecting.sort(key=lambda brick: brick.y_min)

                if len(intersecting) > 1:
                    line += ' ??? '
                else:
                    line += f' {intersecting[0].label} '
            else:
                line += ' ... '

        line += f' {z:03}'

        print(line)

    line = ''

    for i in range(x_max + 1):
        line += ' --- '

    line += ' 000' + ' ' * 4

    for i in range(y_max + 1):
        line += ' --- '

    line += ' 000' + ' ' * 4

    print(line)
    print()


def print_bricks_z(bricks, z):
    x_max = max([brick.x_max for brick in bricks])
    y_max = max([brick.y_max for brick in bricks])

    line = ' x' + ' ' * (((x_max + 1) * 5) - 1) + 'y'
    print(line)

    line = ''

    for i in range(x_max + 1):
        line += f' {i}   '

    print(line)

    for y in range(y_max + 1):
        line = ''

        for i in range(x_max + 1):
            intersecting: List[Brick]
            intersecting = [brick for brick in bricks if brick.crosses_z(z) and brick.crosses_y(y) and brick.crosses_x(i)]

            if intersecting:
                intersecting.sort(key=lambda brick: brick.x_min)

                if len(intersecting) > 1:
                    line += ' ??? '
                else:
                    line += f' {intersecting[0].label} '
            else:
                line += ' ... '

        line += f' {y}' + ' ' * 4

        print(line)
    print()