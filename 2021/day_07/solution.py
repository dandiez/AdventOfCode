from unittest import TestCase

import numpy as np


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines[0].split(',')]  # parse here...
    return inp


def part_1(inp):
    arr = np.array(inp)
    return find_minimum(arr, calc_fuel)


def find_minimum(arr, func):
    _min = min(arr)
    _max = max(arr)
    _min_fuel_found = 999999999999
    for n in range(_min, _max + 1):
        fuel = func(arr, n)
        if fuel < _min_fuel_found:
            _min_fuel_found = fuel
    return _min_fuel_found


def calc_fuel(arr, pos):
    return np.abs(arr - pos).sum()


def part_2(inp):
    arr = np.array(inp)
    return find_minimum(arr, calc_fuel_2)


def calc_fuel_2(arr, pos):
    deltas = np.abs(arr - pos)
    fuel_cost = (deltas / 2) * (deltas + 1)
    return fuel_cost.sum()


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
    inp = read_input("sample_1")
    self.assertEqual(37, part_1(inp))
    self.assertEqual(168, part_2(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
