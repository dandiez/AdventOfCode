import os
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
    ins = [parse("{}{:d}", line).fixed for line in lines]
    return ins


def get_rot_matrix(n):
    return np.array(
        [
            [cos(np.deg2rad(n)), -sin(np.deg2rad(n))],
            [sin(np.deg2rad(n)), cos(np.deg2rad(n))],
        ]
    )


def part_1(inp):
    xy = np.array((0.0, 0.0))
    d = np.array((1.0, 0.0))

    for (i, n) in inp:
        if i == "F":
            xy += d * n
        if i == "N":
            xy += np.array((0, 1)) * n
        if i == "S":
            xy += np.array((0, -1)) * n
        if i == "E":
            xy += np.array((1, 0)) * n
        if i == "W":
            xy += np.array((-1, 0)) * n
        if i == "L":
            m = get_rot_matrix(n)
            d = m.dot(d)
        if i == "R":
            m = get_rot_matrix(-n)
            d = m.dot(d)

    return abs(xy[0]) + abs(xy[1])


def part_2(inp):
    xy = np.array((10.0, 1.0))
    xys = np.array((0.0, 0.0))

    for (i, n) in inp:
        if i == "F":
            xys += xy * n
        if i == "N":
            xy += np.array((0, 1)) * n
        if i == "S":
            xy += np.array((0, -1)) * n
        if i == "E":
            xy += np.array((1, 0)) * n
        if i == "W":
            xy += np.array((-1, 0)) * n
        if i == "L":
            m = get_rot_matrix(n)
            xy = m.dot(xy)
        if i == "R":
            m = get_rot_matrix(-n)
            xy = m.dot(xy)
    return abs(xys[0]) + abs(xys[1])


def main(input_file):
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(p1)
    # inp = read_input(input_file)
    p2 = part_2(inp)
    print(p2)
    return p1, p2


def test_sample_1(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(25, p1)
    self.assertEqual(286, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_sample_1(TestCase())
    main("full.txt")
