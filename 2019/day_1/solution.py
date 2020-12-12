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
    inp = [int(val) for val in lines]  # parse here...
    return inp


def part_1(inp):
    p_1 = sum((m // 3 - 2 for m in inp))
    return p_1


def part_2(inp):
    tot_f = 0
    for m in inp:
        f = m // 3 - 2
        while f >= 0:
            tot_f += f
            f = f // 3 - 2
    p_2 = tot_f
    return p_2


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(p1)

    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(p2)
    return p1, p2


def test_sample_1(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(2 + 2 + 654 + 33583, p1)
    # self.assertEqual( , p2)
    print("***Tests 1 passed so far***")


def test_sample_2(self):
    input_file = "sample_2.txt"
    p1, p2 = main(input_file)
    # self.assertEqual(2+2+654+33583 , p1)
    self.assertEqual(2 + 966 + 50346, p2)
    print("***Tests 2 passed so far***")


if __name__ == "__main__":
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    main("full.txt")
