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
    top_l = [line.strip() for line in top.split("\n") if line.strip()]
    bottom_l = [line.strip() for line in bottom.split("\n") if line.strip()]
    inp = top_l, bottom_l  # parse here...
    print(top_l)
    print(bottom_l)
    return inp


def get_rules(id, known, source, validation):
    # return all matching so far, i.e., {"aba", "abb", "baa"}
    # print(id, known, source)
    if id in known:
        return known[id]
    if '"' in source[id][0][0]:
        r = {source[id][0][0].strip('"')}
        known[id] = r
        return r
    r = set()
    for rule in source[id]:
        rls_to_combine = []
        for v in rule:
            rls = get_rules(v, known, source, validation)
            rls_to_combine.append(rls)
        for rl_set in itertools.product(*rls_to_combine):

            r.add("".join(rl_set))
    known[id] = r
    return r


def parse_rule(rule):
    return [tuple(r.split()) for r in rule.split("|")]


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    rl, vl = read_input(input_file)
    source = {s.split(": ")[0]: parse_rule(s.split(": ")[1]) for s in rl if s.strip()}
    validation = [v.strip() for v in vl if v.strip()]
    known = dict()
    zero = part_wrapper(1, "0", known, source, validation)
    p1 = sum(s in known["0"] for s in validation)
    p2 = None
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2

def part_wrapper(part, id, known, source, validation):
    if part == 2:
        source["8"] = [('42'), ('42', '8')]
        source["11"] = [('42', '31'), ('42', '11', '31')]
    return get_rules(id, known, source, validation)


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(2, p1)
    # self.assertEqual( , p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    p1, p2 = main("full.txt")
    assert 265 == p1, "no longer passing part 1"
