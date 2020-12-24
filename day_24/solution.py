import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict
import itertools
import numpy as np
from math import cos, sin, pi
import contextlib
from unittest import TestCase

import lark


def read_input(filename="input.txt"):
    with open(filename) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    grammar = r"""
        start: direction (direction)*
        direction: "ne" -> ne
            | "nw" -> nw
            | "se" -> se
            | "sw" -> sw
            | "e" -> e
            | "w" -> w
        _NEWLINE: "\n"
        %import common.WS
        %ignore WS
    """
    class TransformPaths(lark.Transformer):
        start = list
        path = list
        se = lambda self, items: np.array((1, -1))
        sw = lambda self, items: np.array((0, -1))
        ne = lambda self, items: np.array((0, 1))
        nw = lambda self, items: np.array((-1, 1))
        w = lambda self, items: np.array((-1, 0))
        e = lambda self, items: np.array((1, 0))
    parser = lark.Lark(grammar)
    data = []
    for line in lines:
        p = parser.parse(line)
        print(p.pretty())
        d = TransformPaths().transform(p)
        print(d)
        data.append(d)
    return data


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    data = read_input(input_file)
    print(f"Data contains {len(data)} paths")
    tiles = []
    for p in data:
        tile = tuple(sum(p))
        if tile in tiles:
            tiles.remove(tile)
            print(f"tile {tile} was there already. flipping it back.")
        else:
            tiles.append(tile)
            print(f"flipped tile {tile}")

    p1 = len(tiles)
    p2 = None
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual( 10, p1)
    # self.assertEqual( , p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
