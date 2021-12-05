from collections import defaultdict
from unittest import TestCase

import numpy as np


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [line.split(' -> ') for line in lines]  # parse here...
    inp = [((int(a.split(',')[0]), int(a.split(',')[1])),
            (int(b.split(',')[0]), int(b.split(',')[1]))
            ) for a, b in inp]
    return inp


def part_1(inp):
    valid_points = [ppair for ppair in inp if is_horiz_or_vert(ppair)]
    return get_answer(valid_points)


def get_answer(valid_points):
    grid = defaultdict(int)
    for point in get_all_line_points(valid_points):
        grid[point] += 1
    return count_points_with_more_than_2(grid)


def count_points_with_more_than_2(grid):
    count = 0
    for val in grid.values():
        if val >= 2:
            count += 1
    return count


def get_all_line_points(all_ppairs):
    for ppair in all_ppairs:
        yield from get_line_points(ppair)


def get_line_points(ppair):
    a, b = ppair
    if a == b:
        yield a
        return
    _a, _b = np.array(a), np.array(b)
    delta = _b - _a
    distance = abs(delta[0]) + abs(delta[1])
    unit_vector = delta / distance
    if 0 < abs(unit_vector[0]) < 1:
        unit_vector = unit_vector * 2
        distance = distance // 2
    for n in range(0, distance + 1):
        point = _a + n * unit_vector
        int_point = (int(point[0]), int(point[1]))
        yield int_point


def is_horiz_or_vert(point_pair):
    a, b = point_pair
    if a[0] == b[0] or a[1] == b[1]:
        return True
    return False


def part_2(inp):
    valid_points = inp
    return get_answer(valid_points)


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    # inp = read_input("sample_1")
    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
