import sys

from shared import input


def transpose(l):
    return list(zip(*l))


def roll(line):
    # print(line)
    rounds = [0]
    cubes = []
    new_line = []

    for i, item in enumerate(line):
        if item == 'O':
            rounds[-1] += 1
        elif item == '#':
            cubes.append(i)
            rounds.append(0)

    # print(rounds, cubes)

    for i in range(len(line)):
        if i in cubes:
            new_line.append('#')
            cubes.remove(i)
            rounds = rounds[1:]

            continue

        if rounds[0]:
            new_line.append('O')
            rounds[0] -= 1
        else:
            new_line.append('.')

    # print(new_line)
    # print()

    return new_line


def score(line):
    return sum([i + 1 for i, c in enumerate(reversed(line)) if c == 'O'])


def north(table):
    return transpose([roll(list(line)) for line in transpose(table)])


def west(table):
    return [roll(list(line)) for line in table]


def south(table):
    return transpose([list(reversed(roll(list(reversed(line))))) for line in transpose(table)])


def east(table):
    return [list(reversed(roll(list(reversed(line))))) for line in table]


# 103333 is right
#
# 95160 is too low
# 97241 is right
def main(filename):
    table = input.readfile(filename)
    print_table(table)
    tables = []
    target_cycles = 1_000_000_000

    while True:
        table = cycle(table)
        table_id = calculate_table_id(table)
        ids = [tid for tid, _ in tables]

        if table_id in ids:
            print((table_id, table))
            repeat_offset = ids.index(table_id)
            repeat_length = len(tables) - repeat_offset
            print(f'Repeat detected: {repeat_length} after initial run of {repeat_offset}')
            break
        else:
            tables.append((table_id, table))
            print((table_id, table))

    target_table = tables[(target_cycles - repeat_offset) % repeat_length + repeat_offset - 1][1]
    print_table(target_table)

    scores = [score(line) for line in transpose(target_table)]

    print(scores)
    print(f'Total: {sum(scores)}')


def cycle(table):
    return east(south(west(north(table))))


def print_table(table):
    for line in table:
        print(''.join(line))

    print()


def calculate_table_id(table):
    id = 0

    for y, row in enumerate(table):
        for x, c in enumerate(row):
            if c == 'O':
                id += 2**(y * len(row) + x)

    return id


if __name__ == '__main__':
    main(sys.argv[1])