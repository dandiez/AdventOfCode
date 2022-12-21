from __future__ import annotations
import dataclasses
from unittest import TestCase
from scipy.optimize import fsolve


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
        match self.operator:
            case "-": return a - b
            case "+": return a + b
            case "*": return a * b
            case "/": return a / b
            case z: raise ValueError(f"unknown operator: {z}")


def read_input(filename="input") -> dict[str, Monkey]:
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


@dataclasses.dataclass
class Monkeys:
    _monkeys: dict[str, Monkey]
    _raw: list[str]

    @classmethod
    def from_inp(cls, inp: list[str]):
        ms = [Monkey.from_line(val) for val in inp]
        return cls(
            _monkeys={m.name: m for m in ms},
            _raw=inp
        )

    def p2_reset(self):
        ms = [Monkey.from_line(val) for val in self._raw]
        self._monkeys = {m.name: m for m in ms}
        self._monkeys["root"].operator = "-"
        self._monkeys["humn"] = Monkey(name="humn")

    def get_root(self, human: int):
        self.p2_reset()
        self._monkeys["humn"].result = human[0]
        return self._monkeys["root"].get_result(self._monkeys)


def part_1(inp):
    monkeys = Monkeys.from_inp(inp)
    return monkeys._monkeys["root"].get_result(monkeys._monkeys)


def part_2(inp):
    monkeys = Monkeys.from_inp(inp)
    h = fsolve(monkeys.get_root, 100000000)
    return int(h[0])


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


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(301, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
