import copy
from ast import literal_eval
from enum import Enum
from unittest import TestCase

class State(Enum):
    in_right_order = 1
    not_in_right_order = 2
    not_known = 3

def read_input(filename="input"):
    with open(filename) as f:
        pairs = [p.strip().split("\n") for p in f.read().split("\n\n") if p.strip()]
    inp = [(literal_eval(p[0]), literal_eval(p[1])) for p in pairs]  # parse here...
    return inp

def is_mixed_types(left, right):
     return _is_left_int_right_list(left, right) or _is_left_int_right_list(right, left)


def _is_left_int_right_list(left, right):
    return isinstance(left, int) and isinstance(right, list)

def _int_to_list(value):
    if isinstance(value, int):
        return [value]
    return value

def is_in_right_order(left, right) -> State:

    if is_mixed_types(left, right):
        left = _int_to_list(left)
        right = _int_to_list(right)
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return State.not_known
        elif left < right:
            return State.in_right_order
        else:
            return State.not_in_right_order
    # both are lists
    state = State.not_known
    while (state is State.not_known) and left and right:
        l = left.pop(0)
        r = right.pop(0)
        state = is_in_right_order(l, r)
    if state is not State.not_known:
        print(state)
        return state
    if not left and not right:
        print(state)
        return state
    if not left:
        print(State.in_right_order)
        return State.in_right_order
    elif not right:
        print(State.not_in_right_order)
        return State.not_in_right_order

def part_1(inp):
    pairs = {i: pair for i, pair in zip(range(1, len(inp)+1), inp)}
    return sum(i for i,p in pairs.items() if is_in_right_order(*p) is State.in_right_order)

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
    self.assertEqual(13, part_1(inp))
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
