import sys

from record import Record, get_runs
from shared import input


def brute_force(record):
    unknowns = record.springs.count('?')
    combos = 2**unknowns
    valid = 0

    print(f'Combos to brute force: {combos}')

    for i in range(combos):
        springs = []
        combo = list(bin(i)[2:].zfill(unknowns))
        # print(combo)

        for c in record.springs:
            if c == '?':
                springs.append('.' if combo[0] == '0' else '#')
                combo = combo[1:]
            else:
                springs.append(c)

        runs = [len(run) for _, run in get_runs(springs, '#')]

        if runs == record.damage_runs:
            # print(record, i, springs, runs)
            valid += 1

    print(f'Found {valid} valid combos')

    return valid


def calculate_paths(record, previous_paths, current):
    paths = {}

    length = previous_paths[0]

    # print(f'Previous paths: {sum(previous_paths[1].values())} {previous_paths[1]}')

    for start in previous_paths[1].keys():
        for s in current[1]:
            if s > start + length:
                if '#' not in record.springs[start + length:s]:
                    if s not in paths:
                        paths[s] = previous_paths[1][start]
                    else:
                        paths[s] += previous_paths[1][start]

    return current[0], paths


def calculate_combinations(record, possible_run_locations):
    paths = (possible_run_locations[0][0], {s: 1 for s in possible_run_locations[0][1]})

    for i, possible_run_location in enumerate(possible_run_locations[1:]):
        # print(f'{i + 1}/{len(possible_run_locations) - 1}: ', end='')
        paths = calculate_paths(record, paths, possible_run_location)
        # print(paths)

    # print(paths)

    return sum(paths[1].values())


# 7402 is right
#
# 3384337640277 is right
def main(filename):
    lines = [line.split(' ') for line in input.readfile(filename)]
    folds = 5
    records = [
        Record(
            list(springs) + (['?'] + list(springs)) * (folds - 1),
            [int(c) for c in damaged.split(',')] * folds,
        )
        for springs, damaged in lines
    ]

    total = 0
    max_combinations = {'combinations': 0}

    for i, record in enumerate(records):
        print(f'{i + 1}: {record}')
        possible_run_locations = record.get_possible_run_locations()

        print(possible_run_locations)

        combinations = calculate_combinations(record, possible_run_locations)
        print(f'Combinations: {combinations:,}')

        # brute_force_combinations = brute_force(record)
        #
        # if combinations != brute_force_combinations:
        #     print(f'Brute force returned something different: {brute_force_combinations}')
        #     break

        print()

        if combinations > max_combinations['combinations']:
            max_combinations['record_num'] = i + 1
            max_combinations['record'] = record
            max_combinations['possible_run_locations'] = possible_run_locations
            max_combinations['combinations'] = combinations

        total += combinations

    print(f'Total: {total:,}')
    print()
    print('Max:')
    print(f"{max_combinations['record_num']}: {max_combinations['record']}")
    print(max_combinations['possible_run_locations'])
    print(f"Combinations: {max_combinations['combinations']:,}")


if __name__ == '__main__':
    main(sys.argv[1])
