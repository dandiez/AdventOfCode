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
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [list(line.replace(" ", "")) for line in lines]
    # parse here...
    return inp


def exp_to_num(expr, p2=False):
    return eval(_eval(expr, p2=p2)[0])


def _eval(ex: [str], p2: bool):
    # recursive evaluation of only one thing at a time, in order of precedence
    if ")" in ex:
        cl = ex.index(")")  # leftmost close bracket
        op = max(tuple(i for i, c in enumerate(ex[:cl]) if c == "("))  # matching bracket
        return _eval(
            ex[:op]
            + _eval(ex[op + 1:cl], p2)
            + ex[cl + 1:],
            p2)
    if p2:
        if "+" in ex:
            pos = ex.index("+")
            return _eval(
                ex[:pos - 1]
                + [str(eval("".join(ex[pos - 1:pos + 2])))]
                + ex[pos + 2:],
                p2)
    if len(ex) >= 3:
        return _eval([str(eval("".join(ex[:3])))] + ex[3:], p2)
    assert len(ex) == 1, "ups"
    return ex


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = sum(exp_to_num(expr) for expr in inp)
    p2 = sum(exp_to_num(expr, p2=True) for expr in inp)
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(437, p1)
    self.assertEqual(1445, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    p1, p2 = main("full.txt")
    assert 4696493914530 == p1
