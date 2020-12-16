import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict
import itertools
import numpy as np
from math import cos, sin, pi
from unittest import TestCase


def read_input(filename="full.txt"):
    with open(filename) as f:
        inp = f.read()

    return inp


def part_1(inp):
    a, b = inp.split("nearby tickets:")
    r, m = a.split("your ticket:")
    rules = [line.strip() for line in r.splitlines() if line.strip()]
    mine = [line.strip() for line in m.splitlines() if line.strip()]
    other = [line.strip() for line in b.splitlines() if line.strip()]
    rules_dict = dict()
    my_ticket = [int(val) for val in mine[0].split(",")]
    print("My ticket", my_ticket)
    for r in rules:
        c, rng = r.split(": ")
        r1, r2 = rng.split(" or ")
        r1min, r1max = r1.split("-")
        r2min, r2max = r2.split("-")
        rules_dict[c] = [(int(r1min), int(r1max)), (int(r2min), int(r2max))]
    other_tickets = [[int(v) for v in line.split(",")] for line in other]
    print("other tickets", other_tickets)
    print(rules_dict)
    bad = 0
    good_tickets = copy.deepcopy(other_tickets)
    for t in other_tickets:
        print("ticket is ", t)
        for val in t:
            is_ok = False
            for rule in rules_dict.values():
                r1a, r1b = rule[0]
                r1c, r1d = rule[1]
                if ((r1a <= val <= r1b) or (r1c <= val <= r1d)):
                    is_ok = True
                    break
            if not is_ok:
                bad += val
                good_tickets.remove(t)
    print("good tickets:", good_tickets)
    ok_fields = {pos: list(rules_dict.keys()) for pos, _ in enumerate(my_ticket)}
    print("ok fileds", ok_fields)
    for t in good_tickets:
        for pos, num in enumerate(t):
            for rule_name, rule in rules_dict.items():
                r1a, r1b = rule[0]
                r1c, r1d = rule[1]
                if not ((r1a <= num <= r1b) or (r1c <= num <= r1d)):
                    print("Removing field", pos, num, rule_name, rule)
                    ok_fields[pos].remove(rule_name)
    print("OK Fields:")
    mapped = {}
    updated = True
    p2 = 1
    while updated:
        updated = False
        for k, v in ok_fields.items():
            if len(v) == 1:
                found = v[0]
                mapped[found] = my_ticket[k]
                if found.startswith("departure"):
                    p2 *= my_ticket[k]
                for ff in ok_fields.values():
                    try:
                        ff.remove(found)
                    except ValueError:
                        pass
                updated = True
    print(mapped)
    print("P2:", p2)
    p_1 = bad
    return p_1


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
    self.assertEqual(71, p1)
    # self.assertEqual( , p2)
    print("***Tests 1 passed so far***")

    input_file = "sample_2.txt"
    # p1, p2 = main(input_file)
    # self.assertEqual( , p1)
    # self.assertEqual( , p2)
    print("***Tests 2 passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
