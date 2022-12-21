from __future__ import annotations
import dataclasses
from unittest import TestCase


@dataclasses.dataclass
class Monkey:
    name: str
    result: int = None
    left: int = None
    right: int = None
    operator: str = None

    @classmethod
    def from_line(cls, line: str):
        name, eq = [a.strip() for a in line.split(": ")]
        try:
            left, operator, right = [a.strip() for a in eq.split(" ")]
            result = None
        except ValueError:
            result = int(eq)
            left, operator, right = None, None, None
        return cls(name, result, left, right, operator)

    def get_result(self, all_monkeys: dict[str, Monkey]):
        if self.result is None:
            calculated = self.calculate(all_monkeys)
            self.result = calculated
        return self.result

    def calculate(self, all_monkeys: dict[str, Monkey]):
        a = all_monkeys[self.left].get_result(all_monkeys)
        b = all_monkeys[self.right].get_result(all_monkeys)
        return eval(f"{a}{self.operator}{b}")


def read_input(filename="input") -> dict[str, Monkey]:
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [Monkey.from_line(val) for val in lines]
    return {m.name: m for m in inp}


def part_1(inp):
    return inp["root"].get_result(inp)


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
    self.assertEqual(152, part_1(inp))
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