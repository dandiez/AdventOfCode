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
    inp = [[parse("{}{:d}", leg) for leg in cable.split(",")] for cable in lines]  # parse here...
    return inp


def v(x, y):
    return np.array((x, y))


directions = {"U": v(0, 1), "D": v(0, -1), "R": v(1, 0), "L": v(-1, 0)}


def part_1(inp):
    min_md, cable_paths, common_grids = calculate_crossings(inp)
    p_1 = min_md
    return p_1


def calculate_crossings(inp):
    cable_paths = []
    for cable in inp:
        used_grid = []
        pos = v(0, 0)
        for (letter, num) in cable:
            d = directions[letter]
            for n in range(num):
                pos += d
                used_grid.append(tuple(pos))
        cable_paths.append(used_grid)
    min_md = np.inf
    common_grids = set.intersection(*[set(cable) for cable in cable_paths])
    for inter in common_grids:
        md = abs(inter[0]) + abs(inter[1])
        min_md = min(min_md, md)
    return min_md, cable_paths, common_grids


def part_2(inp):
    _, cable_paths, common_grids = calculate_crossings(inp)
    min_d = np.inf
    for g in common_grids:
        d = sum(cable.index(g) + 1 for cable in cable_paths)
        min_d = min(min_d, d)
    p_2 = min_d
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
    input_file = "sample_0.txt"
    p1, p2 = main(input_file)
    self.assertEqual(6, p1)
    self.assertEqual(30, p2)
    print("***Tests 1 passed so far***")

    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(159, p1)
    self.assertEqual(610, p2)
    print("***Tests 1 passed so far***")

    input_file = "sample_2.txt"
    p1, p2 = main(input_file)
    self.assertEqual(135, p1)
    self.assertEqual(410, p2)
    print("***Tests 2 passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
