import copy
import itertools
from unittest import TestCase


def read_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines[0].split(",")  # parse here...
    inp = [int(v) for v in inp]
    return inp


def part_1(inp, noun=12, verb=2):
    if noun is not None:
        inp[1] = noun
    if verb is not None:
        inp[2] = verb
    p = 0
    while True:
        # print(inp)
        instruction = inp[p]
        # print(op)
        if instruction == 1:  # sum
            try:
                params = inp[p + 1:p + 4]
                inp[params[2]] = inp[params[0]] + inp[params[1]]
                p += len(params) + 1
            except (KeyError, IndexError):
                return None
        elif instruction == 2:  # multiplication
            try:
                params = inp[p + 1:p + 4]
                inp[params[2]] = inp[params[0]] * inp[params[1]]
                p += len(params) + 1
            except (KeyError, IndexError):
                return None
        elif instruction == 99:  # end program
            break
        else:
            return None
            # raise Exception(f"unknown {instruction}")

    p_1 = inp[0]
    return p_1


def part_2(inp):
    for (n, v) in itertools.product(range(100), repeat=2):
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
