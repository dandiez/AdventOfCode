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
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines  # parse here...
    return inp


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)

    food = []
    for line in inp:
        ingr, alerg = line.split(" (contains ")
        ingr_list = ingr.split(" ")
        alerg, _ = alerg.split(")")
        alerg_list = [a.strip() for a in alerg.split(",") if a.strip()]
        food.append((ingr_list, alerg_list))

    alg_dict = defaultdict(list)
    for f in food:
        ing, alg = f
        print(ing)
        print(alg)
        for al in alg:
            alg_dict[al].append(set(ing))
    print("alg dict", alg_dict)

    known=dict()

    did_change=True
    while did_change:
        did_change=False
        for al, ings in alg_dict.items():
            print("checking ", al, ings)
            if al in known.values():
                print("skipping ", al)
                continue
            unique = set.intersection(*ings)
            if len(unique)==1:
                print("fund unique:", unique)
                val = unique.pop()
                unique.add(val)
                known[val]=al
                did_change=True
                break
        if did_change:
            new_alg_dict = dict()
            for al, ings in alg_dict.items():
                new_ings = []
                for ing_set in ings:
                    new_ings.append(ing_set.difference(unique))
                new_alg_dict[al]=new_ings
            alg_dict=new_alg_dict

    print(known)
    print(alg_dict)
    print("Food ",food)
    known_set = set(known.keys())
    c=0
    for f in food:
        ings, algs = f
        c += len(set(ings).difference(known_set))

    p1 = c
    print(known)
    s = ",".join(dict(sorted(known.items(), key=lambda item: item[1])).keys())
    p2 = s
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual( 5, p1)
    self.assertEqual("mxmxvkd,sqjhc,fvjkl" , p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
