import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict
import itertools
import numpy as np
from math import cos, sin, pi
import contextlib
import functools
from unittest import TestCase


def read_input(filename="input.txt"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


@functools.lru_cache(None)
def neighbours(p, dim):
    n = set()
    zero = (0,) * dim
    for dp in itertools.product((-1, 0, 1), repeat=dim):
        if dp != zero:
            n.add(tuple(map(sum, zip(p, dp))))
    return n


def part_1_and_2(lines, dim, num_cycles=6):
    x_ini = len(lines[0])
    y_ini = len(lines)
    g = set()
    for x, line in enumerate(lines):
        for y, val in enumerate(line):
            if val == "#":
                g.add((x, y) + (0,) * (dim - 2))

    def run_sim(g, dim):
        g_new = set()
        grids_to_check = set()
        for p in g:
            grids_to_check = grids_to_check.union((neighbours(p, dim)))
        for p in grids_to_check:
            active_n = len(g.intersection(neighbours(p, dim)))
            if p in g and active_n in (2, 3):
                g_new.add(p)
            elif p not in g and active_n == 3:
                g_new.add(p)
        return g_new

    for i in range(num_cycles):
        g = run_sim(g, dim)
        print(".", end="")
    print("")
    p_1 = len(g)
    return p_1


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1_and_2(inp, 3)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = part_1_and_2(inp, 4)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(112, p1)
    self.assertEqual(848, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
