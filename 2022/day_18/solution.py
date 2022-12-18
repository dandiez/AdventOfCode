import dataclasses
from unittest import TestCase

import numpy as np


def get_six_directions():
    pos_units = [np.array([1,0,0]), np.array([0,-1,0]), np.array([0,0,-1])]
    neg_units = [-a for a in pos_units]
    yield from pos_units
    yield from neg_units

@dataclasses.dataclass(frozen=True)
class Point:
    coords: tuple[int, int, int]

    @classmethod
    def from_string(cls, s: str):
        return cls(
            tuple(
                [int(n) for n in s.split(",")]
            ))

    def neighbours(self):
        center = np.array(self.coords)
        for d in get_six_directions():
            yield Point(tuple(center+d))



def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    inp = [Point.from_string(val) for val in lines]  # parse here...
    return inp


def part_1(inp):
    all_points = set(inp)
    return sum(n not in all_points for p in all_points for n in p.neighbours())


def part_2(inp):
    pass


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
    self.assertEqual(64, part_1(inp))
    pass


def test_sample_2(self):
    # inp = read_input("sample_1")
    # self.assertEqual(1, part_1(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
