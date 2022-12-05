import dataclasses
from collections import deque
from unittest import TestCase

NUM_STACKS = 9


@dataclasses.dataclass
class Stacks(dict[int, deque]):
    NUM_STACKS = 9

    @classmethod
    def from_raw(cls, raw):
        stacks = cls()
        for k in range(1, 1 + cls.NUM_STACKS):
            stacks[k] = deque()
        for line in raw.split("\n"):
            if not line:
                break
            for id, pos in zip(
                range(1, cls.NUM_STACKS + 1), range(1, 4 * (NUM_STACKS + 1), 4)
            ):
                try:
                    value = line[pos].strip()
                except IndexError:
                    break
                if value and not isinstance(value, int):
                    stacks[id].appendleft(value)
        return stacks

    def get_answer(self):
        return "".join([v[-1] for v in self.values() if v])


@dataclasses.dataclass
class Instruction:
    quantity: int
    from_id: int
    to_id: int

    @classmethod
    def from_string(cls, string):
        chunked = string.split()
        return Instruction(int(chunked[1]), int(chunked[3]), int(chunked[5]))


def read_input(filename="input"):
    with open(filename) as f:
        raw = f.read()
    boxes, movements = raw.split("\n\n")[:2]
    stacks = Stacks.from_raw(boxes)
    instructions = [
        Instruction.from_string(string.strip())
        for string in movements.splitlines()
        if string.strip()
    ]
    return stacks, instructions


def part_1(inp: tuple[Stacks, list[Instruction]]):
    stacks, instructions = inp
    for instruction in instructions:
        for q in range(instruction.quantity):
            box = stacks[instruction.from_id].pop()
            stacks[instruction.to_id].append(box)
    return stacks.get_answer()


def part_2(inp):
    stacks, instructions = inp
    for instruction in instructions:
        temp = []
        for q in range(instruction.quantity):
            box = stacks[instruction.from_id].pop()
            temp.append(box)
        temp.reverse()
        for box in temp:
            stacks[instruction.to_id].append(box)
    return stacks.get_answer()


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
    self.assertEqual("CMZ", part_1(inp))


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual("MCD", part_2(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
