import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict
import itertools
import numpy as np
from math import cos, sin, pi
from unittest import TestCase
from sympy import Matrix, lcm


def read_input(filename="input.txt"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    arrive = int(lines[0])
    buses_1 = [int(v) for v in lines[1].split(",") if v != "x"]
    buses_2 = dict()
    for n, b in enumerate(lines[1].split(",")):
        if b == "x":
            continue
        buses_2[n] = int(b)
    return arrive, buses_1, buses_2


def part_1(inp):
    arrive, buses, _ = inp
    rem = [arrive % bus for bus in buses]
    # print(rem)
    if 0 in rem:
        return 0
    available = [arrive - r + bus for (r, bus) in zip(rem, buses)]
    # print(available)
    wait = [a - arrive for a in available]
    min_wait = min(wait)
    ind = wait.index(min_wait)
    best = buses[ind] * min_wait
    p_1 = best
    return p_1


def part_2(inp):
    _, _, buses = inp
    print(buses)
    # sort from longest period down, such that we check buses with longer intervals first
    r = {v: k for k, v in sorted(buses.items(), reverse=True, key=lambda item: item[1])}
    longest = list(r.keys())[0]
    offset_longest = r[longest]
    assert longest == max(buses.values())
    # first possible time for the bus with the longest period (ID) is the period "longest" minus its offset
    t = longest - offset_longest
    # next possible time is a period afterwards (longest), so start with dt = longest
    dt = longest
    print("longest", longest, "offset", offset_longest)
    # by definition, we have chosen the bus with the longest period as a reference, therefore
    # the time t will always be ok for it.
    ok = [longest]
    while True:
        all_good = True
        for v, k in r.items():
            if v in ok:
                # because we keep choosing the dt such that the ok buses fit to the time, we don't need
                # to check for them. Deleting them from the dictionary midloop breaks the loop.
                continue
            if (t + k) % v != 0:
                # for a bus with period v and offset k, the t is a good answer only if
                # we wait the offset after t, i.e., (t+k) and that returns a time that happens to be a multiple
                # of the bus' period v (i.e., the bus is back).
                # If this is not the case, then the time t is not a good answer and we should check the next
                # opportunity after dt.
                all_good = False
                break
            else:
                # We found a time t for which a new bus is correctly aligned.
                # The question is, how long will it be until these buses meet eachother again at the correct offsets?
                # Say the first bus arrives every 4min and the second every 3min, then every 12min the cycle repeats
                # itself and both buses are in the same relative position to one another. So, if we were checking every
                # 4 minutes, now we can check every 12min (from the current time t which had the buses aligned,
                # meaning, they will continue to stay aligned if we keep checking in these intervals).
                print(t)
                dt *= v  # in general it should probably be the l.c.m., or we might skip the first instance of the time
                ok.append(v)
        if not all_good:
            t += dt
        else:
            return t


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
    self.assertEqual(295, p1)
    self.assertEqual(1068781, p2)
    print("***Tests 1 passed so far***")

    input_file = "sample_2.txt"
    p1, p2 = main(input_file)
    self.assertEqual(3417, p2)
    # self.assertEqual( , p2)
    self.assertEqual(part_2((None, None, {0: 1789, 1: 37, 2: 47, 3: 1889})), 1202161486)
    # self.assertEqual(part_2((None, None, {19: 599, 50: 761})), 1)
    print("Tests passed")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
