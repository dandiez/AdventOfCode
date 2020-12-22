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


def player_1_wins_game(nums1, nums2, is_part_1=True):
    print("playing with ", nums1, nums2)
    nums1 = nums1[:]
    nums2 = nums2[:]
    prev_rounds_1 = []  # list of tuples
    prev_rounds_2 = []

    while nums1 and nums2:
        if tuple(nums1) in prev_rounds_1 or tuple(nums2) in prev_rounds_2:
            return nums1, nums2, True
        prev_rounds_1.append(tuple(nums1))
        prev_rounds_2.append(tuple(nums2))

        player_1_wins = None
        a, b = nums1[0], nums2[0]
        if (a <= (len(nums1) - 1)) and (b <= (len(nums2) - 1)) and not is_part_1:
            #print("Recursing!", nums1, nums2)
            _, _, player_1_wins = player_1_wins_game(nums1[1:a + 1], nums2[1:b + 1])
        else:
            #print("not recursing")
            if a > b:
                player_1_wins = True
            elif b > a:
                player_1_wins = False
            else:
                print("Draw")

        if player_1_wins is None:
            nums1 = nums1[1:]
            nums1.append(a)
            nums2 = nums2[1:]
            nums2.append(b)
        elif player_1_wins:
            nums1 = nums1[1:]
            nums1.extend([a, b])
            nums2 = nums2[1:]
        else:
            nums2 = nums2[1:]
            nums2.extend([b, a])
            nums1 = nums1[1:]

    return nums1, nums2, len(nums1) > len(nums2)


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    nums1, nums2 = read_input(input_file)
    nums1, nums2, p_1_wins = player_1_wins_game(nums1, nums2, is_part_1=True)
    win_list = nums1 + nums2
    score = sum(n * i for n, i in zip(win_list, range(len(win_list), 0, -1)))
    p1 = score


    # part 2
    nums1, nums2 = read_input(input_file)
    nums1, nums2, p_1_wins = player_1_wins_game(nums1, nums2, is_part_1=False)
    win_list = nums1 + nums2
    score = sum(n * i for n, i in zip(win_list, range(len(win_list), 0, -1)))
    p2 = score
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(306, p1)
    self.assertEqual(291, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    p1, p2 = main("full.txt")
    assert p1 == 33434
    assert p2 == 31657
