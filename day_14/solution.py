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
        lines = f.read()
    inp = lines  # parse here...
    return inp


def part_1(inp):
    blocks = [block.strip() for block in inp.split("mask = ") if block.strip()]
    L = []
    for b in blocks:
        lines = b.split("\n")
        mask = lines[0]
        ops = []
        for s in lines[1:]:
            # print(s)
            a, n = search("mem[{:d}] = {:d}", s).fixed
            ops.append((a, n))
        L.append((mask, ops))
    mem = dict()
    for i in L:
        mask = i[0]
        ops = i[1]
        for a, n in ops:
            b = '{:036b}'.format(n)
            for j, c in enumerate(mask):
                if c != "X":
                    # print(c)
                    b = list(b)
                    b[j] = c
                    b = "".join(b)
            mem[a] = b
    tot = 0
    for val in mem.values():
        tot += int(val, 2)

    p_1 = tot
    return p_1


def part_2(inp):
    blocks = [block.strip() for block in inp.split("mask = ") if block.strip()]
    L = []
    for bin_val_to_set in blocks:
        lines = bin_val_to_set.split("\n")
        mask = lines[0]
        ops = []
        for s in lines[1:]:
            # print(s)
            mem_a, val_to_set = search("mem[{:d}] = {:d}", s).fixed
            ops.append((mem_a, val_to_set))
        L.append((mask, ops))
    mem = dict()
    for i in L:
        mask = i[0]
        ops = i[1]
        for mem_a, val_to_set in ops:
            bin_mem = '{:036b}'.format(mem_a)
            for j, c in enumerate(mask):
                if c in ["1", "X"]:
                    bin_mem = replace_char(bin_mem, c, j)
            xs = bin_mem.count("X")
            for m in range(2 ** xs):
                aaa = bin_mem
                f = "{:0" + str(xs) + "b}"
                bb = f.format(m)
                q = 0
                for k, cc in enumerate(aaa):
                    if cc == "X":
                        aaa = replace_char(aaa, bb[q], k)
                        q += 1
                mem[aaa] = val_to_set

    tot = 0
    for val in mem.values():
        tot += val

    p_2 = tot
    return p_2


def replace_char(my_string, c, position):
    my_string = list(my_string)
    my_string[position] = c
    my_string = "".join(my_string)
    return my_string


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
    # p1, p2 = main(input_file)
    # self.assertEqual(165, p1)
    # self.assertEqual( , p2)
    print("***Tests 1 passed so far***")

    input_file = "sample_2.txt"
    p1, p2 = main(input_file)
    self.assertEqual(208, p2)
    # self.assertEqual( , p2)
    print("***Tests 2 passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
