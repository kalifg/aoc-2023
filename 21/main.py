import sys
import time
import timeit

from typing import List, Dict, Tuple
from plot import Plot, PlotType, print_plots, reset_plots
from shared import input


# 3722 is right
#
# 614864614526014 is right
def main(filename: str):
    lines = input.readfile(filename)
    # print(lines)

    plots = [[Plot(PlotType(c)) for c in line] for line in lines]
    # print(plots)

    start = connect_plots(plots)

    m = len(plots[0])
    n = len(plots)

    can_step_on_map = set()

    for row in plots:
        for plot in row:
            if plot.can_step_on:
                can_step_on_map.add(plot.location)

    # print(can_step_on_map)

    # print_plots(plots)
    # map_plot(start, depth=64, cache=plot_cache)

    starts = [start.location]
    # steps = 6
    steps = n // 2 + 2 * n
    # steps = 500
    # steps = 26501365

    print(f'Steps: {steps}')

    # neighbor_cache = {}

    total_start_time = time.time()

    values = []

    # for i in range(steps):
    #     start_time = time.time()
    #     starts = traverse_plots(starts, m, n, can_step_on_map)
    #     values.append(len(starts))
    #     end_time = time.time() - start_time
    #     print(f'Step: {i}, length: {len(starts)}, traversal time: {end_time}s')
    #     # print()

    values = [4, 8, 16, 24, 35, 47, 58, 74, 90, 111, 130, 151, 176, 199, 228, 252, 287, 314, 354, 390, 412, 462, 489, 550, 580, 645, 684, 740, 786,
        842, 888, 945, 1005, 1071, 1130, 1193, 1247, 1322, 1379, 1456, 1518, 1603, 1669, 1760, 1823, 1923, 1991, 2090, 2160, 2257, 2327, 2431, 2498, 2611, 2677,
        2804, 2864, 3003, 3064, 3202, 3275, 3444, 3545, 3722, 3814, 3988, 4082, 4260, 4324, 4491, 4560, 4747, 4816, 5010, 5077, 5275, 5348, 5545, 5621, 5827, 5894,
        6115, 6182, 6411, 6480, 6710, 6798, 7018, 7110, 7330, 7438, 7643, 7755, 7963, 8101, 8297, 8455, 8652, 8794, 8992, 9144, 9339, 9490,
        9697, 9849, 10060, 10209, 10448, 10590, 10831, 10972, 11223, 11375, 11612, 11766, 11996, 12166, 12401, 12588, 12821, 13020, 13247, 13454, 13687,
        13886, 14117, 14332, 14558, 14778, 15012, 15234, 15468, 15703, 15943, 16185, 16405, 16664, 16884, 17141, 17368, 17652, 17872, 18145, 18369, 18653, 18867,
        19146, 19362, 19667, 19892, 20210, 20396, 20729, 20931, 21274, 21484, 21830, 22058, 22366, 22600, 22916, 23154, 23471, 23742, 24068, 24329,
        24658, 24887, 25240, 25462, 25829, 26049, 26439, 26660, 27070, 27269, 27695, 27897, 28314, 28523, 28932, 29138, 29544, 29752, 30171,
        30373, 30828, 31013, 31480, 31675, 32127, 32330, 32844, 33139, 33676, 33952, 34470, 34744, 35266, 35476, 35947, 36139, 36652,
        36848, 37371, 37566, 38087, 38298, 38799, 39019, 39530, 39730, 40270, 40475, 41035, 41239, 41786, 42029, 42553, 42801, 43316, 43592, 44077, 44356, 44836, 45170,
        45626, 46004, 46459, 46792, 47241, 47593, 48037, 48376, 48852, 49189, 49670, 49995, 50532, 50838, 51354, 51668, 52202, 52539, 53039, 53379, 53861, 54227, 54716, 55113, 55597,
        56012, 56481, 56906, 57384, 57795, 58266, 58704, 59160, 59603, 60072, 60515, 60980, 61446, 61918, 62394, 62823, 63329, 63758, 64256, 64694, 65241, 65662, 66187, 66610, 67155,
        67554, 68088, 68485, 69068, 69478, 70078, 70428, 71044, 71421, 72046, 72436, 73063, 73480, 74040, 74462, 75038, 75468, 76045, 76527, 77113, 77576, 78171, 78575, 79206, 79593, 80250,
        80628, 81323, 81699, 82428, 82763, 83515, 83851, 84586, 84934, 85655, 85997, 86705, 87054, 87779, 88117, 88900, 89210, 90005, 90334, 91100, 91433, 92292,
        92781, 93678, 94138,]

    pairs = []

    for i in range(3):
        x = n // 2 + n * i
        pairs.append((x, values[x - 1]))

    print(pairs)

    x0, y0 = pairs[0]
    x1, y1 = pairs[1]
    x2, y2 = pairs[2]

    y01 = (y1 - y0) / (x1 - x0)
    y12 = (y2 - y1) / (x2 - x1)
    y012 = (y12 - y01) / (x2 - x0)

    n = 26501365
    total_endpoints = y0 + y01 * (n - x0) + y012 * (n - x0) * (n - x1)

    # print(values)
    # differences = values
    #
    # while any(differences):
    #     differences = differentiate(differences)
    #     print(differences)

    # print_plots(plots)

    print(f'Total execution time: {time.time() - total_start_time}s')
    print(start)

    # total_endpoints = len(starts)

    print(f'There are {total_endpoints} end-points')


def count_plots(plots: List[List[Plot]]) -> int:
    total = 0

    for row in plots:
        for plot in row:
            if plot.is_end_point:
                total += 1

    return total


def traverse_plots(starts: List[Tuple[int, int]], m: int, n: int, can_step_on_map: set(Tuple[int, int])) -> List[Plot]:
    plots = set()

    for i, start in enumerate(starts):
        # start_time = time.time()
        x, y = start

        neighbors = [
            ((x - 1, y), (y % n, (x - 1) % m)),
            ((x + 1, y), (y % n, (x + 1) % m)),
            ((x, y - 1), ((y - 1) % n, x % m)),
            ((x, y + 1), ((y + 1) % n, x % m)),
        ]

        # print(start, neighbors, neighbor_templates)

        for absolute_point, relative_point in neighbors:
            if relative_point not in can_step_on_map:
                continue

            plots.add(absolute_point)

        # if ((i % 100000) == 0):
        #     print(f'Time to check start: {time.time() - start_time}s')

    return plots


def connect_plots(plots: List[List[Plot]]) -> Plot:
    start = None

    for y, row in enumerate(plots):
        for x, plot in enumerate(row):
            if plot.plot_type == PlotType.START:
                start = plot

            plot.location = x, y
            plot.unique_id = y * len(plots) + x

            if x > 0:
                plot.west = plots[y][x - 1]
            else:
                plot.west = plots[y][-1]

            if x < len(row) - 1:
                plot.east = plots[y][x + 1]
            else:
                plot.east = plots[y][0]

            if y > 0:
                plot.north = plots[y - 1][x]
            else:
                plot.north = plots[-1][x]

            if y < len(plots) - 1:
                plot.south = plots[y + 1][x]
            else:
                plot.south = plots[0][x]

    return start


if __name__ == '__main__':
    main(sys.argv[1])