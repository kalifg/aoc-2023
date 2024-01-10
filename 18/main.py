import sys

from enum import Enum
from shared import input
from typing import Tuple, List, Dict


class Direction(Enum):
    R = 0
    D = 1
    L = 2
    U = 3


class Edge:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int], color: str):
        self.start = start
        self.end = end
        self.color = color

    def __repr__(self):
        return f'<{self.start}->{self.end}: {self.color}>'

    @property
    def direction(self) -> Direction:
        match self.start, self.end:
            case ((x1, y1), (x2, y2)) if y1 == y2 and x1 <= x2:
                return Direction.R
            case ((x1, y1), (x2, y2)) if y1 == y2 and x1 > x2:
                return Direction.L
            case ((x1, y1), (x2, y2)) if x1 == x2 and y1 <= y2:
                return Direction.D
            case ((x1, y1), (x2, y2)) if x1 == x2 and y1 > y2:
                return Direction.U

    def outside_edges(self, previous_direction: Direction, next_direction: Direction) -> Dict[Direction, Tuple[Tuple[int, int], Tuple[int, int]]]:
        (x1, y1), (x2, y2) = self.start, self.end

        match previous_direction, self.direction, next_direction:
            case (Direction.U, Direction.R, Direction.D) | (Direction.D, Direction.L, Direction.U):
                return {
                    Direction.U: ((x1, y1), (x2 + 1, y2)),
                    Direction.D: ((x1 + 1, y1 + 1), (x2, y2 + 1)),
                }
            case (Direction.U, Direction.R, Direction.U) | (Direction.D, Direction.L, Direction.D):
                return {
                    Direction.U: ((x1, y1), (x2, y2)),
                    Direction.D: ((x1 + 1, y1 + 1), (x2 + 1, y2 + 1)),
                }
            case (Direction.U, Direction.L, Direction.D) | (Direction.D, Direction.R, Direction.U):
                return {
                    Direction.U: ((x1 + 1, y1), (x2, y2)),
                    Direction.D: ((x1, y1 + 1), (x2 + 1, y2 + 1)),
                }
            case (Direction.U, Direction.L, Direction.U) | (Direction.D, Direction.R, Direction.D):
                return {
                    Direction.U: ((x1 + 1, y1), (x2 + 1, y2)),
                    Direction.D: ((x1, y1 + 1), (x2, y2 + 1)),
                }
            case (Direction.L, Direction.U, Direction.R) | (Direction.R, Direction.D, Direction.L):
                return {
                    Direction.L: ((x1, y1 + 1), (x2, y2)),
                    Direction.R: ((x1 + 1, y1), (x2 + 1, y2 + 1)),
                }
            case (Direction.L, Direction.U, Direction.L) | (Direction.R, Direction.D, Direction.R):
                return {
                    Direction.L: ((x1, y1 + 1), (x2, y2 + 1)),
                    Direction.R: ((x1 + 1, y1), (x2 + 1, y2)),
                }
            case (Direction.L, Direction.D, Direction.R) | (Direction.R, Direction.U, Direction.L):
                return {
                    Direction.L: ((x1, y1), (x2, y2 + 1)),
                    Direction.R: ((x1 + 1, y1 + 1), (x2 + 1, y2)),
                }
            case (Direction.L, Direction.D, Direction.L) | (Direction.R, Direction.U, Direction.R):
                return {
                    Direction.L: ((x1, y1), (x2, y2)),
                    Direction.R: ((x1 + 1, y1 + 1), (x2 + 1, y2 + 1)),
                }


def generate_normal_map(edges: List[Edge]) -> Dict[Direction, Direction]:
    normal1 = {
        Direction.R: Direction.U,
        Direction.D: Direction.R,
        Direction.L: Direction.D,
        Direction.U: Direction.L,
    }

    normal2 = {
        Direction.R: Direction.D,
        Direction.D: Direction.L,
        Direction.L: Direction.U,
        Direction.U: Direction.R,
    }

    match edges[0].direction, edges[-1].direction:
        case (Direction.R, Direction.U) | (Direction.L, Direction.D) | (Direction.U, Direction.L) | (Direction.D, Direction.L):
            return normal1
        case (Direction.R, Direction.D) | (Direction.L, Direction.U) | (Direction.U, Direction.R) | (Direction.D, Direction.R):
            return normal2


# 44436 is right
#
# 106941819907437 is right
def main(filename):
    lines = input.readfile(filename)
    edges = []
    volume = 0

    original_start = start = (0, 0)

    for line in lines:
        # Input type 1
        # direction, length, color = line.split(' ')
        #
        # direction = getattr(Direction, direction)
        # length = int(length)

        # Input type 2
        _, _, color = line.split(' ')
        length, direction = int(color[2:-2], 16), color[-2]
        direction = Direction(int(direction))

        end = None

        match direction:
            case Direction.R:
                end = (start[0] + length, start[1])
            case Direction.L:
                end = (start[0] - length, start[1])
            case Direction.U:
                end = (start[0], start[1] - length)
            case Direction.D:
                end = (start[0], start[1] + length)

        edge = Edge(start, end, color)

        print(f'{direction} {length}: {edge}')
        edges.append(edge)
        start = end

    if start != original_start:
        raise ValueError('Path is not closed')

    normal_map = generate_normal_map(edges)

    print()
    for j, edge in enumerate(edges):
        i = (j - 1) % len(edges)
        k = (j + 1) % len(edges)

        outside_edges = edge.outside_edges(edges[i].direction, edges[k].direction)
        start, end = outside_edges[normal_map[edge.direction]]

        print(f'{edge}: {start, end}')
        volume += start[0] * end[1] - end[0] * start[1]

    volume /= 2
    print(f'Volume: {volume}')
    print(f'Volume: {volume:,}')


if __name__ == '__main__':
    main(sys.argv[1])
