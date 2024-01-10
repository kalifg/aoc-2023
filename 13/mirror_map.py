def transpose(mirror_map):
    return list(zip(*mirror_map))


class MirrorMap:
    def __init__(self, mirror_map):
        self.mirror_map = mirror_map

    def __repr__(self):
        return "\n".join([''.join(row) for row in self.mirror_map])

    def get_reflections(self):
        reflection_points = {
            'rows': get_vertical_reflections(self.mirror_map),
            'columns': get_vertical_reflections(transpose(self.mirror_map))
        }

        return reflection_points

    def remove_smudge(self, x, y):
        copy = [m[:] for m in self.mirror_map]
        copy[y][x] = '.' if copy[y][x] == '#' else '#'

        return MirrorMap(copy)


def get_vertical_reflections(mirror_map):
    reflection_points = []
    previous_line = mirror_map[0]

    for i, line in enumerate(mirror_map[1:]):
        if line == previous_line:
            reflection_point = (i, i + 1)
            bounds = verify_reflection(mirror_map, reflection_point)

            if bounds:
                reflection_points.append((
                    bounds[0],
                    reflection_point[0],
                    reflection_point[1],
                    bounds[1]
                ))

        previous_line = line

    return reflection_points


def verify_reflection(mirror_map, reflection_point):
    i, j = reflection_point

    while True:
        if mirror_map[i] != mirror_map[j]:
            return False

        i -= 1
        j += 1

        if i < 0 or j >= len(mirror_map):
            break

    return i + 1, j - 1

