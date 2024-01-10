import sys

from mirror_map import MirrorMap
from shared import input


def calculate_score(reflections):
    return (sum([b + 1 for _, b, _, _ in reflections['columns']]) +
            100 * sum([b + 1 for _, b, _, _ in reflections['rows']]))

# 35360 is right
#
# 36755 is right
def main(filename):
    mirror_maps = []
    current_map = []
    lines = input.readfile(filename)

    for line in lines:
        if not line:
            mirror_maps.append(MirrorMap(current_map))
            current_map = []
        else:
            current_map.append(list(line))

    mirror_maps.append(MirrorMap(current_map))

    total_score = 0

    for m in mirror_maps:
        smudge, m2, reflections = fix_smudge(m)

        print(m2)
        print(f'Smudge: {smudge}')
        print(reflections)

        score = calculate_score(reflections)
        print(f'Score: {score}')

        total_score += score
        print()

    print(f'Total Score: {total_score}')


def fix_smudge(m):
    original_reflections = m.get_reflections()

    for y in range(len(m.mirror_map)):
        for x in range(len(m.mirror_map[y])):
            m2 = m.remove_smudge(x, y)

            reflections = m2.get_reflections()
            reflections = {
                'rows': [row for row in reflections['rows'] if row not in original_reflections['rows']],
                'columns': [column for column in reflections['columns'] if column not in original_reflections['columns']],
            }

            if reflections['rows'] or reflections['columns']:
                return (x, y), m2, reflections


if __name__ == '__main__':
    main(sys.argv[1])