import contextlib
import copy
import itertools
from dataclasses import dataclass
from unittest import TestCase


def read_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines[0].split(",")  # parse here...
    inp = [int(v) for v in inp]
    return inp


@dataclass
class Code:
    op_code: int
    modes: int


class IntcodeComputer:

    def __init__(self, memory):
        self.memory = memory
        self.position = 0
        self.max_cycles = 10000
        self.stop = False

    def read_and_skip(self):
        value = self.memory[self.position]
        self.position += 1
        return value

    def execute(self):
        num_cycles = 0
        while num_cycles <= self.max_cycles and not self.stop:
            self.process_instruction()

    def process_instruction(self):
        code_raw = self.read_and_skip()
        code = self.parse_code(code_raw)
        if code.op_code == 1:
            self.process_sum(code)
        elif code.op_code == 2:
            self.process_mult(code)
        elif code.op_code == 99:
            self.stop = True

    def process_sum(self, code):
        p1 = self.read_and_skip()
        p2 = self.read_and_skip()
        out = self.read_and_skip()
        self.memory[out] = self.memory[p1] + self.memory[p2]

    def process_mult(self, code):
        p1 = self.read_and_skip()
        p2 = self.read_and_skip()
        out = self.read_and_skip()
        self.memory[out] = self.memory[p1] * self.memory[p2]

    @staticmethod
    def parse_code(code_raw):
        op_code = code_raw % 100
        modes = code_raw // 100
        code = Code(op_code=op_code, modes=modes)
        return code


def part_1(inp, noun=12, verb=2):
    if noun is not None:
        inp[1] = noun
    if verb is not None:
        inp[2] = verb
    p = 0
    computer = IntcodeComputer(inp)
    computer.execute()

    p_1 = inp[0]
    return p_1


def part_2(inp):
    for (n, v) in itertools.product(range(100), repeat=2):
        with contextlib.suppress(Exception):
            p_1 = part_1(copy.deepcopy(inp), noun=n, verb=v)
        if p_1 == 19690720:
            return 100 * n + v
    p_2 = None
    return p_2


def main(input_file, **kwargs):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp, **kwargs)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file, noun=None, verb=None)
    self.assertEqual(30, p1)
    self.assertEqual(3500, part_1([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], noun=None, verb=None))
    self.assertEqual(2, part_1([1, 0, 0, 0, 99], noun=None, verb=None))
    self.assertEqual(2, part_1([2, 3, 0, 3, 99], noun=None, verb=None))
    self.assertEqual(2, part_1([2, 4, 4, 5, 99, 0], noun=None, verb=None))
    self.assertEqual(30, part_1([1, 1, 1, 4, 99, 5, 6, 0, 99], noun=None, verb=None))
    # self.assertEqual(1202, part_1([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], noun=12, verb=2))
    # self.assertEqual(  , p2)
    print("***Tests 1 passed so far***")


if __name__ == "__main__":
    test_sample_1(TestCase())
    main("input")
