import sortedcontainers
import sys

from block import Block, reset_blocks, print_blocks, Path
from shared import input
from typing import List


# 1008 is too high
# 774 is too high
# 740 is too high
# 722 is right
#
# 894 is right
def main(filename, start_location, end_location):
    lines = input.readfile(filename)

    if '' in lines:
        lines = lines[:lines.index('')]

    blocks = [[Block(c, (x, y)) for x, c in enumerate(line)] for y, line in enumerate(lines)]

    print(f'Starting location: {start_location}')
    # starts = [blocks[start_location[1]][start_location[0]]]
    starts = [block for row in blocks for block in row]
    # ends = [blocks[end_location[1]][end_location[0]]]
    ends = starts[:]

    total_paths = 0

    for start in starts:
        for end in starts:
            total_paths += 1
            end = dijkstra(blocks, start, end)

            path_to_load = []
            current = end

            while current.x != start.x or current.y != start.y:
                path_to_load.append(blocks[current.y][current.x])
                current = current.previous_block

            path_to_load.append(start)
            path_to_load = list(reversed(path_to_load))
            path_to_load = Path(path_to_load)
            # print(path_to_load)
            # erase_previous_lines()
            load_path(blocks, path_to_load)

            print(f'Paths: {total_paths}')
            print()
            print_blocks(blocks)

            if total_paths < len(starts) * len(ends):
                erase_previous_lines(len(blocks) + 3)

    print(f'Total paths: {total_paths}')


def load_path(blocks, path):
    reset_blocks(blocks)

    for i, block in enumerate(path.blocks):
        if i == 0:
            direction = None
        else:
            direction = block.get_direction(path[:i + 1])

        block.direction = direction


def dijkstra(blocks: List[List[Block]], start: Block, end: Block):
    min_straight = 4
    max_straight = 10

    start, unvisited = connect_nodes(blocks, end, max_straight, min_straight, (start.x, start.y))

    visited = []
    visited_count = 0
    unvisited_count = 0
    current = start

    while True:
        # if visited_count % 100 == 0 or unvisited_count % 100 == 0:
        #     print(f'visited: {visited_count}, unvisited: {unvisited_count}')
        #     erase_previous_lines()

        if current.x == end.x and current.y == end.y and current.last_turned >= min_straight:
            return current

        neighbors = current.neighbors

        for direction, block in neighbors.items():
            if not block:
                continue

            distance = block.heat_loss + current.tentative_distance

            if distance < block.tentative_distance:
                block.previous_block = current
                block.tentative_distance = distance
                unvisited.add(block)
                unvisited_count += 1

        visited.append(current)
        visited_count += 1

        try:
            current = unvisited.pop(0)
        except IndexError:
            raise Exception('No path found!')

        unvisited_count -= 1


def erase_previous_lines(num_lines=1):
    sys.stdout.write(f'\x1b[{num_lines}A')
    sys.stdout.write('\r')
    sys.stdout.flush()


def connect_nodes(blocks, end, max_straight, min_straight, start_location=(0, 0)):
    nodes = {}
    unvisited = sortedcontainers.SortedList()

    for row in blocks:
        for block in row:
            for direction in ['left', 'right', 'up', 'down']:
                for last_turned in range(1, max_straight + 1):
                    new_block = Block(block.heat_loss, (block.x, block.y))
                    new_block.direction = direction
                    new_block.last_turned = last_turned
                    nodes[(block.x, block.y, direction, last_turned)] = new_block

    for (x, y, direction, last_turned), node in nodes.items():
        if x == end.x and y == end.y:
            continue

        if x > 0:
            if direction == 'right':
                pass
            elif (direction == 'up' or direction == 'down') and last_turned < min_straight:
                pass
            elif direction == 'left' and last_turned > max_straight - 1:
                pass
            else:
                node.left = nodes[(x - 1, y, 'left', last_turned + 1 if direction == 'left' else 1)]

        if x < len(blocks[0]) - 1:
            if direction == 'left':
                pass
            elif (direction == 'up' or direction == 'down') and last_turned < min_straight:
                pass
            elif direction == 'right' and last_turned > max_straight - 1:
                pass
            else:
                node.right = nodes[(x + 1, y, 'right', last_turned + 1 if direction == 'right' else 1)]

        if y > 0:
            if direction == 'down':
                pass
            elif (direction == 'left' or direction == 'right') and last_turned < min_straight:
                pass
            elif direction == 'up' and last_turned > max_straight - 1:
                pass
            else:
                node.up = nodes[(x, y - 1, 'up', last_turned + 1 if direction == 'up' else 1)]

        if y < len(blocks) - 1:
            if direction == 'up':
                pass
            elif (direction == 'left' or direction == 'right') and last_turned < min_straight:
                pass
            elif direction == 'down' and last_turned > max_straight - 1:
                pass
            else:
                node.down = nodes[(x, y + 1, 'down', last_turned + 1 if direction == 'down' else 1)]

    start = Block(0, start_location)
    start.tentative_distance = 0
    start.last_turned = 0

    if start_location[0] < len(blocks[0]) - 1:
        start.right = nodes[(start_location[0] + 1, start_location[1], 'right', 1)]

    if start_location[0] > 0:
        start.left = nodes[(start_location[0] - 1, start_location[1], 'left', 1)]

    if start_location[1] < len(blocks) - 1:
        start.down = nodes[(start_location[0], start_location[1] + 1, 'down', 1)]

    if start_location[1] > 0:
        start.up = nodes[(start_location[0], start_location[1] - 1, 'up', 1)]

    return start, unvisited


if __name__ == '__main__':
    x_start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    y_start = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    x_end = int(sys.argv[4]) if len(sys.argv) > 4 else -1
    y_end = int(sys.argv[5]) if len(sys.argv) > 5 else -1

    main(sys.argv[1], (x_start, y_start), (x_end, y_end))