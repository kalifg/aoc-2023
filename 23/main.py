import sys

from enum import Enum
from typing import List, Dict, Tuple

from shared import input


class Direction(Enum):
    E = 'east'
    W = 'west'
    N = 'north'
    S = 'south'


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors: List[Tuple[Node, int]]
        self.neighbors = []
        self.symbol = '?'

    def __repr__(self):
        return f'<{self.symbol} ({self.x}, {self.y})>'


class Forest(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = '#'


class Path(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = '.'


class Slope(Node):
    def __init__(self, x, y, direction):
        self.direction = direction
        super().__init__(x, y)

        match direction:
            case Direction.W:
                self.symbol = '<'
            case Direction.E:
                self.symbol = '>'
            case Direction.N:
                self.symbol = '^'
            case Direction.S:
                self.symbol = 'v'


# 2162 is right
#
# 5977 is too low
# 6081 is not right
# 6334 is right
def main(filename: str):
    lines = input.readfile(filename)
    nodes = create_nodes(lines)
    connect_nodes(nodes)

    start = nodes[0][1]
    end = nodes[-1][-2]

    # nodes = condense_graph(nodes, start)

    # start = nodes[0][1]

    # start = nodes[0]
    # end = nodes[-1]

    paths = {
        'paths': [],
        'longest_length': 0,
        'longest_path': None,
    }

    traverse_nodes(start, end, [], set(), paths)

    # print(paths)

    for path in paths['paths']:
        print(path)

    print()

    path = paths['longest_path']

    print()
    print(path)
    # print_path(path, nodes)
    # print(f'There were {len(paths)} paths')

    print(f'Longest: {path_length(path)} steps')
    print()

    pass


# def condense_graph(nodes: List[List[Node]], start):
#     graph: List[Node]
#     graph = []
#
#     for row in nodes:
#         for node in row:
#             if isinstance(node, Forest):
#                 continue
#
#             graph.append(node)
#
#     for node in graph:
#         original_neighbors = node.neighbors
#         weight = 1
#         previous = node
#         node.neighbors = []
#
#         for neighbor, original_weight in original_neighbors:
#             neighbors = [(n, w) for n, w in neighbor.neighbors if n != previous]
#             previous = neighbor
#
#             while 0 < len(neighbors) < 2:
#                 n, w = neighbors[0]
#                 weight += w
#                 neighbors = [(n1, w1) for n1, w1 in n.neighbors if n1 != previous]
#                 previous = n
#
#             for n, w in neighbors:
#                 node.neighbors.append((n, weight + 1))
#
#     return graph


def path_length(path):
    return sum([weight for node, weight in path])


def print_path(path: List[Node], nodes: List[List[Node]]):
    for row in nodes:
        for node in row:
            if node == path[0]:
                print('S', end='')
            elif node in path:
                print('O', end='')
            else:
                print(node.symbol, end='')

        print()


def traverse_nodes(start: Node, end: Node, previous: List[Node], previous_set: set[Node], paths: Dict[str, int|List[Node]]):
    while True:
        eligible_neighbors = [(node, weight) for (node, weight) in start.neighbors if node not in previous_set]

        if not eligible_neighbors:
            return

        if len(eligible_neighbors) == 1:
            node, weight = eligible_neighbors[0]

            if node == end:
                break

            previous_set.add(start)
            previous += [(start, weight)]
            start = node
        else:
            break

    previous_set.add(start)

    for node, weight in eligible_neighbors:
        if node == end:
            paths['paths'].append(previous + [(start, weight), (end, 0)])
            if path_length(previous) > paths['longest_length']:
                paths['longest_path'] = previous + [(start, weight), (end, 0)]
                paths['longest_length'] = path_length(previous)
                print(f'Found new longest path (length {path_length(previous) + weight})')
        else:
            traverse_nodes(node, end, previous + [(start, weight)], previous_set.copy(), paths)


def simple_connect(node: Node, nodes: List[List[Node]]):
    x, y = node.x, node.y
    neighbors = []
    current_weight = 1

    if x > 0 and (not isinstance(node, Slope) or node.direction == Direction.W):
        west = nodes[y][x - 1]

        if isinstance(west, Path) or (isinstance(west, Slope) and west.direction != Direction.E):
            neighbors.append((west, current_weight))

    if x < len(nodes[0]) - 1 and (not isinstance(node, Slope) or node.direction == Direction.E):
        east = nodes[y][x + 1]

        if isinstance(east, Path) or (isinstance(east, Slope) and east.direction != Direction.W):
            neighbors.append((east, current_weight))

    if y > 0 and (not isinstance(node, Slope) or node.direction == Direction.N):
        north = nodes[y - 1][x]

        if isinstance(north, Path) or (isinstance(north, Slope) and north.direction != Direction.S):
            neighbors.append((north, current_weight))

    if y < len(nodes) - 1 and (not isinstance(node, Slope) or node.direction == Direction.S):
        south = nodes[y + 1][x]

        if isinstance(south, Path) or (isinstance(south, Slope) and south.direction != Direction.N):
            neighbors.append((south, current_weight))

    node.neighbors = neighbors


def connect_node(node, nodes):
    simple_connect(node, nodes)

    previous_neighbors = node.neighbors[:]
    node.neighbors = []
    seen = set([node])

    for current_node, current_weight in previous_neighbors:
        seen.add(current_node)

        while True:
            x, y = current_node.x, current_node.y
            neighbors = []

            if x > 0 and (not isinstance(current_node, Slope) or current_node.direction == Direction.W):
                west = nodes[y][x - 1]

                if isinstance(west, Path) or (isinstance(west, Slope) and west.direction != Direction.E):
                    if west not in seen:
                        neighbors.append((west, current_weight))
                        seen.add(west)

            if x < len(nodes[0]) - 1 and (not isinstance(node, Slope) or node.direction == Direction.E):
                east = nodes[y][x + 1]

                if isinstance(east, Path) or (isinstance(east, Slope) and east.direction != Direction.W):
                    if east not in seen:
                        neighbors.append((east, current_weight))
                        seen.add(east)

            if y > 0 and (not isinstance(node, Slope) or node.direction == Direction.N):
                north = nodes[y - 1][x]

                if isinstance(north, Path) or (isinstance(north, Slope) and north.direction != Direction.S):
                    if north not in seen:
                        neighbors.append((north, current_weight))
                        seen.add(north)

            if y < len(nodes) - 1 and (not isinstance(node, Slope) or node.direction == Direction.S):
                south = nodes[y + 1][x]

                if isinstance(south, Path) or (isinstance(south, Slope) and south.direction != Direction.N):
                    if south not in seen:
                        neighbors.append((south, current_weight))
                        seen.add(south)

            if len(neighbors) != 1:
                node.neighbors.append((current_node, current_weight))
                break
            else:
                current_node = neighbors[0][0]
                current_weight += 1


def connect_nodes(nodes):
    for row in nodes:
        for node in row:
            if isinstance(node, Forest):
                continue

            node: Node
            connect_node(node, nodes)

            # if len(node.neighbors) == 1:
            #     node.neighbors = strongly_connect(node, nodes, 1)
            # else:
            #     for neighbor in node.neighbors:
            #         neighbor[0].neighbors = strongly_connect(neighbor[0], nodes, neighbor[1], False)


def create_nodes(lines):
    nodes = []

    for y, row in enumerate(lines):
        nodes.append([])

        for x, c in enumerate(row):
            match c:
                case '#':
                    node = Forest(x, y)
                case '.':
                    node = Path(x, y)
                case '>':
                    # node = Slope(x, y, Direction.E)
                    node = Path(x, y)
                case '<':
                    # node = Slope(x, y, Direction.W)
                    node = Path(x, y)
                case '^':
                    # node = Slope(x, y, Direction.N)
                    node = Path(x, y)
                case 'v':
                    # node = Slope(x, y, Direction.S)
                    node = Path(x, y)

            nodes[-1].append(node)

    return nodes


if __name__ == '__main__':
    main(sys.argv[1])