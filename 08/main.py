import itertools
import math
import re
import sys
from typing import List

from shared import input
from node import Node


def process_lines(lines):
    directions = lines[0]
    node_map = {origin: Node(origin, destinations) for (origin, destinations) in [process_line(line) for line in lines[2:]]}

    for name, node in node_map.items():
        node.left = node_map[node.left]
        node.right = node_map[node.right]

    return directions, node_map


def process_line(line):
    pattern = r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)'
    matches = re.match(pattern, line)

    return matches.group(1), (matches.group(2), matches.group(3))


def traverse_map(map, directions):
    currents: List[Node] = [node for name, node in map.items() if node.start_node]
    step_counts = []

    for current in currents:
        steps = 0

        for dir in itertools.cycle(directions):
            steps += 1
            print(f'{steps:,} ({dir}): {current.name}->{current.take_str(dir)}')
            current = current.take(dir)

            if current.end_node:
                break

            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\r')
            sys.stdout.flush()

        step_counts.append(steps)

    return step_counts


def main(filename):
    lines = input.readfile(filename)
    directions, map = process_lines(lines)

    print(directions, map)
    print()
    step_counts = traverse_map(map, directions)
    print()
    print(step_counts)
    print(f'{math.lcm(*step_counts):,}')


if __name__ == '__main__':
    main(sys.argv[1])