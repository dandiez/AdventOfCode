import math
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
        blocks = f.read().split("\n\n")
    print(blocks)
    tiles = dict()
    for t in blocks:
        head, body = t.split(":\n")
        _, num = head.split("Tile ")
        tiles[num] = body
        # print(num)
        # print(body)
    inp = tiles
    return inp


def c_to_num(c):
    if c == "#":
        return 1
    elif c == ".":
        return 0
    else:
        raise ValueError


class Tile():
    def __init__(self, num, body):
        self.num = num
        self._raw = body
        self.b = np.array([[c_to_num(c) for c in s] for s in body], int)
        self.rotations = [np.rot90(self.b, k=n) for n in range(4)] + [
            np.rot90(np.fliplr(self.b), k=n) for n in
            range(4)]
        assert len(self.rotations) == 8
        self.position = 0
        self.location = None

    def locate(self, location):
        self.location = location


def validate(grid, tiles_dict):
    pass


def get_next_empty(grid, size):
    for r in range(size):
        for c in range(size):
            if grid[r, c] is None:
                print("Next empty is", (r, c))
                return (r, c)


def get_rotated_tile(pos, tiles_dict):
    return tiles_dict[pos[0]].rotations[pos[1]]


def lr_fit(left, right, tiles_dict):
    left_rc = get_rotated_tile(left, tiles_dict)[:, -1]
    right_lc = get_rotated_tile(right, tiles_dict)[:, 0]
    if all(
            left_rc == right_lc
    ):
        return True
    return False


def tb_fit(top, bottom, tiles_dict):
    top_br = get_rotated_tile(top, tiles_dict)[-1, :]
    bottom_tr = get_rotated_tile(bottom, tiles_dict)[0, :]
    if all(
            top_br == bottom_tr
    ):
        return True
    return False


def get_candidates(grid, tiles_left, location, size, tiles_dict):
    # print(f"looking for candidates at location {location}")
    all_positions_left = itertools.product(tiles_left, range(8))

    candidates = []
    r, c = location
    if r != 0:
        top_n = grid[(location[0] - 1, location[1])]
    else:
        top_n = None
    if c != 0:
        left_n = grid[(location[0], location[1] - 1)]
    else:
        left_n = None
    for pos in all_positions_left:
        if top_n is not None:
            if not tb_fit(top_n, pos, tiles_dict):
                continue
        if left_n is not None:
            if not lr_fit(left_n, pos, tiles_dict):
                continue
        candidates.append(pos)

    # print("Candidates found: ", candidates)
    return candidates


def fits(one, another):
    if one is None:
        return True
    return all(one == another)


def solve(grid, tiles_left, size, tiles_dict):
    # print("\nsolving with grid", len([v for k, v in grid.items() if v is not None]))
    # print("Tiles left are", tiles_left)
    if not tiles_left:
        return True
    location = get_next_empty(grid, size)
    potential_positions = get_candidates(grid, tiles_left, location, size, tiles_dict)
    while potential_positions:
        # print(f"potential positions at location {location} are: {potential_positions}")
        t = potential_positions.pop()
        grid[location] = t
        new_tiles_left = [ti for ti in tiles_left if t[0] != ti]
        # print("trying position ", t)
        # print("new tiles left are ", new_tiles_left)
        result = solve(grid, new_tiles_left, size, tiles_dict)
        if result:
            # print("solve returns True")
            return True
        else:
            # print("solve returns False")
            grid[location] = None
    return False

    #
    # all_tiles = tiles
    # tiles_left = tiles
    # tiles_dict = {t.num: t for t in tiles}
    # tile_ids = [t.num for t in tiles]
    # grid = np.zeros((s, s))
    #
    # tipos = list(itertools.product(tile_ids, range(4)))
    # assert len(tipos) == len(tile_ids) * 4
    #
    # coord = itertools.product(range(s), repeat=2)
    #
    # print(tipos)
    # print(coord)

    # while tiles_left:
    #     t = tiles_left.pop()
    #     location = place_in_next_empty(grid, t.num)
    #     t.location = location
    #     if not validate(grid, tiles_dict):


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    tiles = list()
    for t, b in inp.items():
        body = [s.strip() for s in b.splitlines() if s.strip()]
        tiles.append(Tile(t, body))
    # for t in tiles:
    #    print(t.b)

    side_length = int(round(math.sqrt(len(tiles))))
    print(side_length)
    tiles_dict = {t.num: t for t in tiles}
    grid = {(r, c): None for r in range(side_length) for c in range(side_length)}
    tiles_left = [t.num for t in tiles]
    solution = solve(grid, tiles_left, side_length, tiles_dict)
    print(grid)
    p1 = int(grid[0, 0][0]) \
         * int(grid[0, side_length - 1][0]) \
         * int(grid[side_length - 1, 0][0]) \
         * int(grid[side_length - 1, side_length - 1][0])

    p2 = None
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(20899048083289, p1)
    # self.assertEqual( , p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
