import copy
import dataclasses
from ast import literal_eval
from enum import Enum
from typing import Any
from unittest import TestCase


class State(Enum):
    in_right_order = 1
    not_in_right_order = 2
    unknown = 3


def read_input(filename="input"):
    with open(filename) as f:
        pairs = [p.strip().split("\n") for p in f.read().split("\n\n") if p.strip()]
    inp = [(literal_eval(p[0]), literal_eval(p[1])) for p in pairs]  # parse here...
    return inp


def is_mixed_types(left, right):
    return _is_left_int_right_list(left, right) or _is_left_int_right_list(right, left)


def _is_left_int_right_list(left, right):
    return isinstance(left, int) and isinstance(right, list)


def int_to_list(value):
    if isinstance(value, int):
        return [value]
    return value


def is_in_right_order(left, right) -> State:
    if is_mixed_types(left, right):
        left = int_to_list(left)
        right = int_to_list(right)
    if isinstance(left, int) and isinstance(right, int):
        return is_in_right_order_ints(left, right)
    return is_in_right_order_lists(left, right)


def is_in_right_order_lists(left: list, right: list) -> State:
    state = State.unknown
    while (state is State.unknown) and left and right:
        l = left.pop(0)
        r = right.pop(0)
        state = is_in_right_order(l, r)
    if state is not State.unknown:
        return state
    if not left and not right:
        return State.unknown
    if not left:
        return State.in_right_order
    return State.not_in_right_order


def is_in_right_order_ints(left: int, right: int) -> State:
    if left == right:
        return State.unknown
    elif left < right:
        return State.in_right_order
    return State.not_in_right_order


def part_1(inp):
    pairs = {i: pair for i, pair in zip(range(1, len(inp) + 1), inp)}
    return sum(
        i for i, p in pairs.items() if is_in_right_order(*p) is State.in_right_order
    )


def part_2(inp):
    packets = []
    for a, b in inp:
        packets.append(a)
        packets.append(b)
    ps = [Packet(p) for p in packets]
    p1 = Packet([[6]])
    p2 = Packet([[2]])
    ps.append(p1)
    ps.append(p2)
    ps.sort()
    return (ps.index(p1) + 1) * (ps.index(p2) + 1)


@dataclasses.dataclass
class Packet:
    p: Any

    def __gt__(self, other):
        if (
            is_in_right_order(copy.deepcopy(self.p), copy.deepcopy(other.p))
            is State.in_right_order
        ):
            return False
        return True


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
    self.assertEqual(13, part_1(inp))
    pass


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(140, part_2(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
