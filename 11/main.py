import sys

from shared import input

expansion_coefficient = 1000000


def get_blank_rows(rows):
    return [idx for idx, row in enumerate(rows) if all([not char.isnumeric() for char in row])]


def print_map(star_map):
    for row in star_map:
        print(''.join(row))

    print()


def transpose(star_map):
    return list(zip(*star_map))


def count_galaxies(row, current_star):
    new_row = []

    for space in row:
        if space == '#':
            new_row.append(str(current_star[0]))
            current_star[0] = current_star[0] + 1
        else:
            new_row.append(space)

    return new_row


def gather_galaxy_coords(star_map):
    galaxy_coords = []

    for y, row in enumerate(star_map):
        for x, space in enumerate(row):
            space: str
            if space.isnumeric():
                galaxy_coords.append((x, y))

    return galaxy_coords


def distance(coord1, coord2):
    delta = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    # print(f'{coord1} -> {coord2} = {delta}')

    return delta


def expand_coord(coord, blank_rows, blank_columns):
    x = coord[0] + sum([expansion_coefficient - 1 for col in blank_columns if col < coord[0]])
    y = coord[1] + sum([expansion_coefficient - 1 for row in blank_rows if row < coord[1]])

    # print(f'{coord} -> {(x, y)}')

    return x, y


def expand_coords(galaxy_coords, blank_rows, blank_columns):
    return [expand_coord(coord, blank_rows, blank_columns) for coord in galaxy_coords]


# 9742154 is right
#
# 411142919886 is right
def main(filename):
    current_galaxy = [1]

    star_map = [count_galaxies(list(line), current_galaxy) for line in input.readfile(filename)]
    print_map(star_map)

    blank_rows = get_blank_rows(star_map)
    print(blank_rows)

    blank_columns = get_blank_rows(transpose(star_map))
    print(blank_columns)

    galaxy_coords = gather_galaxy_coords(star_map)
    print(galaxy_coords)

    galaxy_coords = expand_coords(galaxy_coords, blank_rows, blank_columns)
    print(galaxy_coords)

    total_distance = 0

    for idx, coord1 in enumerate(galaxy_coords):
        for idx2, coord2 in enumerate(galaxy_coords[idx + 1:]):
            # print(f'{idx + 1} -> {idx2 + idx + 2}: ', end='')
            total_distance += distance(coord1, coord2)

    print(total_distance)


if __name__ == '__main__':
    main(sys.argv[1])