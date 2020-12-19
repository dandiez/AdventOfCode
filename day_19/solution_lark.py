from lark import Lark
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


def read_input(filename="input.txt"):
    with open(filename) as f:
        top, bottom = f.read().split("\n\n")
    bottom_l = [line.strip() for line in bottom.split("\n") if line.strip()]
    inp = top, bottom_l
    # print(top)
    # print(bottom_l)
    return inp


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    grammar, validation = read_input(input_file)
    grammar = grammar.replace('8: 42', '8: 42 | 42 8')
    grammar = grammar.replace('11: 42 31', '11: 42 31 | 42 11 31')
    for n, c in zip(range(10), "abcdefghij"):
        grammar = grammar.replace(str(n), c)
    print(grammar)
    lark_parser = Lark(grammar, start="a")
    s = 0
    for v in validation:
        try:
            lark_parser.parse(v)
            print("VALID ", v)
            s += 1
        except Exception:
            pass

    p1 = None
    p2 = s
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_2.txt"
    p1, p2 = main(input_file)
    self.assertEqual(12, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    # test_samples(TestCase())
    p1, p2 = main("full.txt")
    assert 394 == p2, "no longer passing part 2"
