import dataclasses
from typing import Union
from unittest import TestCase


@dataclasses.dataclass
class Range:
    min: int
    max: int

    def __contains__(self, other: Union["Range", int]):
        if isinstance(other, int):
            return (other >= self.min) & (other <= self.max)
        else:
            return other.min in self and other.max in self

    def overlaps_with(self, other: "Range"):
        return self.min in other or self.max in other or other in self

    @classmethod
    def from_string(cls, string: str):
        a, b = string.split("-")
        return Range(int(a), int(b))


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [parse_line(line) for line in lines]
    return inp


def parse_line(line: str):
    a, b = line.split(",")
    return Range.from_string(a), Range.from_string(b)


def part_1(inp):
    return sum((a in b) or (b in a) for a, b in inp)


def part_2(inp):
    return sum(a.overlaps_with(b) for a, b in inp)


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
    self.assertEqual(2, part_1(inp))


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(4, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
