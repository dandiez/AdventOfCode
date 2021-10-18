import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict
import itertools
import numpy as np
from math import cos, sin, pi
from unittest import TestCase


def read_input(filename="input.txt"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines  # parse here...
    return inp


def last_instance(li, val):
    for n in range(len(li) - 1, -1, -1):
        if li[n] == val:
            return n
    return len(li)


def part_1(inp, maxt):
    seen = {v: n for n, v in enumerate(inp[:-1])}
    turn = len(inp) - 1
    num = inp[turn]
    assert num == inp[-1]
    while turn <= maxt - 2:
        # print(turn, num)
        if num in seen.keys():
            new_num = turn - seen[num]
            seen[num] = turn
            num = new_num
        else:
            seen[num] = turn
            num = 0
        turn += 1
    print(turn, num)

    p_1 = num
    print(inp)
    return p_1


def part_2(inp):
    p_2 = None
    return p_2


def main(inp):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    # inp = read_input(input_file)
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")

    # part 2
    # inp = read_input(input_file)
    p2 = part_2(inp)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    # input_file = "sample_1.txt"
    # p1, p2 = main(input_file)
    self.assertEqual(part_1([0, 3, 6], 2020), 436)
    print("***Tests 1 passed so far***")


if __name__ == "__main__":
    assert part_1([0, 3, 6], 2020) == 436
    assert part_1([3, 1, 2], 30000000) == 362
