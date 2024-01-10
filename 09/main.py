import sys

from shared import input


def process_lines(lines):
    return [[int(num) for num in line.split(' ')] for line in lines]


def process_line(line):
    pass


def differentiate(series):
    return [series[i + 1] - series[i] for i in range(len(series) - 1)]


def is_flat(derivative):
    return len(derivative) < 2 or all([num == derivative[0] for num in derivative])


def integrate_forwards(differential, series):
    series.append(series[-1] + differential[-1])

    return series


def integrate_backwards(differential, series):
    series.insert(0, series[0] - differential[0])

    return series


def get_differentials(series):
    differentials = [series]
    derivative = series

    while not is_flat(derivative):
        derivative = differentiate(derivative)
        differentials.append(derivative)

    return differentials


def previous_value(series):
    pass


def next_value(differentials):
    integrals = [integrate_forwards(differentials[-i], differentials[-i - 1]) for i in range(1, len(differentials))]

    return integrals[-1][-1]


def previous_value(differentials):
    integrals = [integrate_backwards(differentials[-i], differentials[-i - 1]) for i in range(1, len(differentials))]

    return integrals[-1][0]


# 1955513104 is right!
#
# 1131 is right!
def main(filename):
    lines = input.readfile(filename)
    data = process_lines(lines)

    print(data)
    print()

    derivatives = [get_differentials(series) for series in data]
    print(derivatives)
    print()

    next_values = [next_value(differentials) for differentials in derivatives]
    print(next_values)
    print(sum(next_values))

    print()

    previous_values = [previous_value(differentials) for differentials in derivatives]
    print(previous_values)
    print(sum(previous_values))


if __name__ == '__main__':
    main(sys.argv[1])