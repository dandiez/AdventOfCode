from __future__ import annotations
import dataclasses
import functools
import math
import typing
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines]  # parse here...
    return inp


@dataclasses.dataclass
class Node:
    orig_pos: int
    value: int
    predecessor: Node = None
    successor: Node = None

    def __repr__(self):
        return f"Numb({self.value=}, {self.orig_pos=})"


@dataclasses.dataclass
class Chain:
    numbs: list[Node]
    zero: Node = None
    length: int = None

    def __iter__(self) -> typing.Iterator[Node]:
        """One full loop from zero."""
        cursor = self.zero
        for _ in range(self.length):
            yield cursor
            cursor = cursor.successor

    def __post_init__(self):
        self.zero = next(n for n in self.numbs if n.value == 0)
        self.length = len(self.numbs)
        self.check_integrity()

    @classmethod
    def from_list_of_ints(cls, ints: list[int]):
        numbs = [Node(i, v) for i, v in enumerate(ints)]
        for pred, succ in zip(numbs, numbs[1:]):
            cls.couple(pred, succ)
        cls.couple(numbs[-1], numbs[0])
        return cls(numbs)

    @staticmethod
    def couple(n1: Node, n2: Node):
        n1.successor = n2
        n2.predecessor = n1

    @classmethod
    def insert_after_cursor(cls, n: Node, cursor: Node):
        old_cursor_successor = cursor.successor
        cls.couple(cursor, n)
        cls.couple(n, old_cursor_successor)

    def mix(self):
        for n in self.numbs:
            self.mix_single(n)
            # self.check_integrity()

    def mix_single(self, n: Node):
        self.couple(n.predecessor, n.successor)
        cursor = n.predecessor
        positions_to_move = abs(n.value) % (self.length - 1)
        if n.value >= 0:
            cursor = self.move_cursor_forward(cursor, positions_to_move)
        else:
            cursor = self.move_cursor_backwards(cursor, positions_to_move)
        self.insert_after_cursor(n, cursor)

    def move_cursor_forward(self, cursor: Node, num_positions: int) -> Node:
        target = cursor
        for k in range(num_positions):
            target = target.successor
        return target

    def move_cursor_backwards(self, cursor: Node, num_positions: int) -> Node:
        target = cursor
        for k in range(num_positions):
            target = target.predecessor
        return target

    def check_integrity(self):
        seen = set()
        t = self.zero
        for _ in range(self.length):
            if (t.value, t.orig_pos) not in seen:
                seen.add((t.value, t.orig_pos))
                t = t.successor
            else:
                raise OverflowError(t, seen)
        assert t is self.zero
        assert len(seen) == self.length


def part_1(inp):
    c = Chain.from_list_of_ints(inp)
    c.mix()
    positions = [1000, 2000, 3000]
    return sum(c.move_cursor_forward(c.zero, pos).value for pos in positions)


def part_2(inp):
    decr_key = 811589153
    c = Chain.from_list_of_ints([i * decr_key for i in inp])
    for _ in range(10):
        c.mix()
    positions = [1000, 2000, 3000]
    return sum(c.move_cursor_forward(c.zero, pos).value for pos in positions)


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
    self.assertEqual(3, part_1(inp))
    c = Chain.from_list_of_ints([0, -4, 1, 2])
    c.mix_single(c.zero.successor)
    self.assertEqual([0, 1, 2, -4], [n.value for n in c])


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
