import sys

from PIL import Image
from node import Node
from shared import input
from typing import List

valid_right = '-7JS'
valid_down = '|JLS'
valid_left = '-LFS'
valid_up = '|7FS'


def process_line(line, line_num):
    return [Node(char, (line_num, idx)) for idx, char in enumerate(list(line))]


def get_adjacent_nodes(current, pipe_matrix):
    loc = current.location

    right = pipe_matrix[loc[0]][loc[1] + 1] if len(pipe_matrix[loc[0]]) > loc[1] + 1 else None
    down = pipe_matrix[loc[0] + 1][loc[1]] if len(pipe_matrix) > loc[0] + 1 else None
    left = pipe_matrix[loc[0]][loc[1] - 1] if loc[1] > 0 else None
    up = pipe_matrix[loc[0] - 1][loc[1]] if loc[0] > 0 else None

    return {
        'right': right if right and current.type in valid_left and right.type in valid_right else None,
        'down': down if down and current.type in valid_up and down.type in valid_down else None,
        'left': left if left and current.type in valid_right and left.type in valid_left else None,
        'up': up if up and current.type in valid_down and up.type in valid_up else None,
    }


def traverse_matrix(pipe_matrix):
    start = None

    for row in pipe_matrix:
        for current in row:
            if current.type == 'S':
                start = current
                start.distance = 0
                break

    print(start)

    if not start:
        raise RuntimeError('No start found!')

    start.add_paths(get_adjacent_nodes(start, pipe_matrix))
    currents: List[(Node, Node)] = [(start, node) for direction, node in start.paths.items() if node]
    print(currents)

    while True:
        for idx, (previous, current) in enumerate(currents):
            current.add_paths(get_adjacent_nodes(current, pipe_matrix))
            currents[idx] = (current, current.get_path(previous))

        for idx, pair in enumerate(currents):
            print(f'{idx}: {pair}')

        if currents[0][1] == currents[1][1]:
            print(f'Max distance: {currents[0][1].distance}')
            current = currents[0][1]
            current.add_paths(get_adjacent_nodes(current, pipe_matrix))
            break

    return start


def area_inside_loop(pipe_matrix):
    area = 0

    for row in pipe_matrix:
        upper = lower = False

        for node in row:
            node.paint(upper, lower)
            upper, lower = node.inside[1], node.inside[3]

        area += sum(1 for node in row if node.is_inside())

    return area


def process_input(lines):
    pipe_matrix = [process_line(line, idx) for idx, line in enumerate(lines)]

    print(pipe_matrix)

    start = traverse_matrix(pipe_matrix)

    print(pipe_matrix)

    print(f'area: {area_inside_loop(pipe_matrix)}')

    node_res = 8

    width = node_res * len(pipe_matrix[0])
    height = node_res * len(pipe_matrix)

    print(f'Creating bitmap of {width}x{height}')
    img = Image.new('RGB', (width, height))

    for j, row in enumerate(pipe_matrix):
        for i, node in enumerate(row):
            node.paint_image(img, (node_res * i, node_res * j))

    img.show('Pipe Maze')

    
# 6897 is right!

# 367 is right!
def main(filename):
    lines = input.readfile(filename)
    process_input(lines)


if __name__ == '__main__':
    main(sys.argv[1])
