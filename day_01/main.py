import unittest
from math import floor


def read_input(input_file):
    with open(input_file) as f:
        return [int(line.strip()) for line in f.readlines() if line.strip()]


def solve(stream, f):
    print(sum(f(mass) for mass in stream))


def get_fuel(mass):
    if mass <= 0:
        return 0
    third = mass / 3
    floored = floor(third)
    return floored - 2


def get_fuel_2(mass):
    total_fuel = get_fuel(mass)
    extra = get_fuel(total_fuel)
    while extra > 0:
        total_fuel += extra
        extra = get_fuel(extra)
    return total_fuel


class _TestSolve(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(2, get_fuel(12))
        self.assertEqual(2, get_fuel(14))
        self.assertEqual(654, get_fuel(1969))
        self.assertEqual(33583, get_fuel(100756))

    def test_samples_2(self):
        self.assertEqual(2, get_fuel_2(14))
        self.assertEqual(966, get_fuel_2(1969))
        self.assertEqual(50346, get_fuel_2(100756))


def main():
    input_file = 'input'
    stream = read_input(input_file)
    solve(stream, get_fuel)
    solve(stream, get_fuel_2)


if __name__ == '__main__':
    main()
