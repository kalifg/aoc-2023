import collections
import sys
from typing import List

sys.path.append('../shared')

from shared import input

Number = collections.namedtuple('Number', ['number', 'position', 'length'])
Part = collections.namedtuple('Part', ['part', 'position', 'numbers'])


def scan_line(line_num, line):
    digits = []
    numbers = []
    parts = []

    for idx, char in enumerate(line):
        if char.isdigit():
            digits.append(char)
        else:
            if digits:
                numbers.append(Number(number=''.join(digits), position=(line_num, idx - len(digits)), length=len(digits)))
                digits = []

            if char != '.':
                parts.append(Part(part=char, position=(line_num, idx), numbers=[]))

    if digits:
        numbers.append(Number(number=''.join(digits), position=(line_num, len(line) - len(digits)), length=len(digits)))

    return numbers, parts


def scan_lines(lines):
    numbers = []
    parts = []

    for idx, line in enumerate(lines):
        new_numbers, new_parts = scan_line(idx, line)
        numbers += new_numbers
        parts += new_parts

    return numbers, parts


def get_bounding_box(number:Number, num_lines, line_length):
    bounding_box = set()
    pos = number.position

    for i in range(number.length):
        if i == 0 and pos[1] > 0:
            if pos[0] > 0:
                bounding_box.add((pos[0] - 1, pos[1] - 1))

            bounding_box.add((pos[0], pos[1] - 1))

            if pos[0] < num_lines - 1:
                bounding_box.add((pos[0] + 1, pos[1] - 1))

        if pos[0] > 0:
            bounding_box.add((pos[0] - 1, pos[1]))

        if pos[0] < num_lines - 1:
            bounding_box.add((pos[0] + 1, pos[1]))

        if i == number.length - 1 and pos[1] < line_length - 1:
            if pos[0] > 0:
                bounding_box.add((pos[0] - 1, pos[1] + 1))

            bounding_box.add((pos[0], pos[1] + 1))

            if pos[0] < num_lines - 1:
                bounding_box.add((pos[0] + 1, pos[1] + 1))

        pos = (pos[0], pos[1] + 1)

    return bounding_box


def is_part_number(number, parts:List[Part], num_lines, line_length):
    bounding_box = get_bounding_box(number, num_lines, line_length)
    # print(number, bounding_box)

    part_found = False

    for part in parts:
        if part.position in bounding_box:
            part.numbers.append(number)
            part_found = True

    return part_found


# 497027 is too low
# 498559 is right!

# 72246648 is right!
def main(filename):
    lines = input.readfile(filename)

    # for line in lines:
    #     print(line)

    numbers, parts = scan_lines(lines)

    # for number in numbers:
    #     print(number)

    # is_part_number has side effects, only run once!
    part_numbers = list(filter(lambda number: is_part_number(number, parts, len(lines), len(lines[0])), numbers))
    # print([part_number.number for part_number in part_numbers])

    # for part in parts:
    #     print(part)

    # print(sum([int(part_number.number) for part_number in part_numbers]))

    gears = list(filter(lambda part: len(part.numbers) == 2, parts))
    # print(gears)

    ratios = [int(gear.numbers[0].number) * int(gear.numbers[1].number) for gear in gears]
    # print(ratios)

    print(sum(ratios))


if __name__ == '__main__':
    main(sys.argv[1])