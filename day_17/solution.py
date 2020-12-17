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

    x_ini = len(lines[0])
    y_ini = len(lines)
    z_ini = 0

    g = []
    for x, line in enumerate(lines):
        for y, val in enumerate(line):
            if val == "#":
                g.append((x, y, z_ini))
    inp = g
    print(g)

    return inp


@functools.lru_cache(None)
def neighbours(x, y, z):
    n = []
    for dx, dy, dz in itertools.product((-1, 0, 1), repeat=3):
        if (dx, dy, dz) != (0, 0, 0):
            n.append((x + dx, y + dy, z + dz))
    return n


def part_1(inp):
    g = inp

    def run_sim(g):
        x_max, x_min, y_max, y_min, z_max, z_min = get_limits(g)
        g_new = []
        for x in range(x_min - 1, x_max + 2):
            for y in range(y_min - 1, y_max + 2):
                for z in range(z_min - 1, z_max + 2):
                    active_n = 0
                    for n in neighbours(x, y, z):
                        if n in g:
                            active_n += 1
                    if (x, y, z) in g and active_n in (2, 3):
                        g_new.append((x, y, z))
                    elif (x, y, z) not in g and active_n == 3:
                        g_new.append((x, y, z))
        return g_new

    for i in range(6):
        g = run_sim(g)

    p_1 = len(g)
    return p_1


def get_limits(g):
    xs = [x for x, y, z in g]
    ys = [y for x, y, z in g]
    zs = [z for x, y, z in g]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    z_min, z_max = min(zs), max(zs)
    return x_max, x_min, y_max, y_min, z_max, z_min


def part_2(inp):
    p_2 = None
    return p_2


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


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(112, p1)
    # self.assertEqual( , p2)
    print("***Tests 1 passed so far***")

    # input_file = "sample_2.txt"
    # p1, p2 = main(input_file)
    # self.assertEqual( , p1)
    # self.assertEqual( , p2)
    print("***Tests 2 passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
