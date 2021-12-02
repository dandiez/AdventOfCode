import dataclasses
from unittest import TestCase

import numpy as np

unit_vectors = {
    "forward": np.array((1, 0)),
    "down": np.array((0, 1)),
    "up": np.array((0, -1)),
}


@dataclasses.dataclass
class Command:
    instruction: str
    quantity: int


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [
        Command(instruction=val.split()[0], quantity=int(val.split()[1]))
        for val in lines
    ]  # parse here...
    return inp


def part_1(inp):
    pos = np.array((0, 0))
    for command in inp:
        delta = unit_vectors[command.instruction] * command.quantity
        pos += delta
    return pos[0] * pos[1]


def part_2(inp):
    pos = np.array((0, 0))
    aim = np.array((0, 0))
    for command in inp:
        delta = unit_vectors[command.instruction] * command.quantity
        if command.instruction in ["up", "down"]:
            aim += delta
        else:
            delta += aim * command.quantity
            pos += delta
    return pos[0] * pos[1]


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
    self.assertEqual(150, part_1(inp))
    self.assertEqual(900, part_2(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
