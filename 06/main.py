import math
import sys
from shared import input
from race import Race

def parse_lines(lines):
    time = process_line(lines[0])
    distance = process_line(lines[1])

    print(time, distance)

    return Race(time, distance)

def process_line(line):
    return int(''.join([num.strip() for num in line.split(':')[1].strip().split(' ') if num]))

# 34934171 is
def main(filename):
    lines = input.readfile(filename)
    race = parse_lines(lines)
    print(race)

    ways_to_win = race.ways_to_win()
    print(ways_to_win)


if __name__ == '__main__':
    main(sys.argv[1])