import unittest
from math import floor


def read_input(input_file):
    with open(input_file) as f:
        yield from (int(line.strip()) for line in f.readlines() if line.strip())

def solve(stream):
    print(sum(get_fuel(mass) for mass in stream))

def get_fuel(mass):
    third = mass / 3
    floored = floor(third)
    return floored - 2

class _TestSolve(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(2, get_fuel(12))
        self.assertEqual(2, get_fuel(14))
        self.assertEqual(654, get_fuel(1969))
        self.assertEqual(33583, get_fuel(100756))

if __name__ == '__main__':
    input_file = 'input'
    stream = read_input(input_file)
    solve(stream)

