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

    _, nums1 = top.split("Player 1:\n")
    nums1 = [int(n) for n in nums1.splitlines() if n.strip()]
    _, nums2 = bottom.split("Player 2:\n")

    nums2 = [int(n.strip()) for n in nums2.splitlines() if n.strip()]

    return nums1, nums2


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    nums1, nums2 = read_input(input_file)

    while nums1 and nums2:
        a, b = nums1[0], nums2[0]
        if a > b:
            nums1 = nums1[1:]
            nums1.extend([a, b])
            nums2 = nums2[1:]
        elif b > a:
            nums2 = nums2[1:]
            nums2.extend([b, a])
            nums1 = nums1[1:]
        else:
            nums1 = nums1[1:].append(a)
            nums2 = nums2[1:].append(b)

    print(nums1)
    print(nums2)
    win_list = nums1 + nums2
    score = sum( n*i for n,i in zip(win_list, range(len(win_list), 0, -1)) )
    p1 = score
    p2 = None
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(306, p1)
    # self.assertEqual( , p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
