import sys

from shared import input
from tile import Tile, join_tiles


# 7517 is right
#
# 7741 is right
def reset_tiles(tiles):
    for row in tiles:
        for tile in row:
            tile.reset()


def cast_beam(start):
    currents = [start]

    while currents:
        for current in currents:
            current: (str, Tile)
            currents.remove(current)

            exits = current[1].enter_from(current[0])

            for new_current in exits:
                if new_current[1]:
                    currents.append(new_current)


def main(filename):
    lines = input.readfile(filename)
    print(lines)

    tiles = [[Tile(c) for c in line] for line in lines]
    join_tiles(tiles)

    starts = []

    for row in tiles:
        for tile in row:
            if tile.y == 0:
                starts.append(('above', tile))

            if tile.x == 0:
                starts.append(('left', tile))

            if tile.x == len(row) - 1:
                starts.append(('right', tile))

            if tile.y == len(tiles) - 1:
                starts.append(('below', tile))

    max_energy = (None, 0)

    for start in starts:
        cast_beam(start)
        energy = get_energy(tiles)

        if energy > max_energy[1]:
            max_energy = ([start], energy)
        elif energy == max_energy[1]:
            max_energy[0].append(start)

        reset_tiles(tiles)

    cast_beam(max_energy[0][0])

    print()
    print_tiles(tiles)
    print()
    print_tiles(tiles, show_direction=False)
    reset_tiles(tiles)

    print(f'Max Energy: {max_energy}')


def print_tile_show_direction(tile):
    if tile.device != '.':
        print(tile.device, end='')
    else:
        if tile.is_energized():
            if tile.entered_from == 'left':
                print('>', end='')
            elif tile.entered_from == 'right':
                print('<', end='')
            elif tile.entered_from == 'above':
                print('v', end='')
            elif tile.entered_from == 'below':
                print('^', end='')
        else:
            print('.', end='')


def get_energy(tiles):
    energy = 0

    for row in tiles:
        for tile in row:
            if tile.is_energized():
                energy += 1

    return energy


def print_tile(tile):
    if tile.is_energized():
        print('#', end='')
    else:
        print('.', end='')


def print_tiles(tiles, show_direction=True):
    for row in tiles:
        for tile in row:
            if show_direction:
                print_tile_show_direction(tile)
            else:
                print_tile(tile)
        print()
    print()


if __name__ == '__main__':
    main(sys.argv[1])