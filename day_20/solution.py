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
    inp = tiles
    return inp


def c_to_num(c):
    if c == "#":
        return 1
    elif c == ".":
        return 0
    else:
        raise ValueError


def get_rot_and_flip_variations(img):
    return [np.rot90(img, k=n) for n in range(4)] + [
        np.rot90(np.fliplr(img), k=n) for n in range(4)
    ]


class Tile:
    def __init__(self, num, body):
        self.num = num
        self._raw = body
        self.b = np.array([[c_to_num(c) for c in s] for s in body], int)
        self.rotations = get_rot_and_flip_variations(self.b)
        assert len(self.rotations) == 8


def get_next_empty(grid, size):
    """Grid will be filled left to right and top to bottom to simplify neighbour checks."""
    for r in range(size):
        for c in range(size):
            if grid[r, c] is None:
                return r, c


def get_rotated_tile(pos, tiles_dict):
    """Return the variation given by the pos tuple.

    pos: (tile_id, rotation_id)
    """
    return tiles_dict[pos[0]].rotations[pos[1]]


def lr_fit(left, right, tiles_dict):
    """Check whether both tiles fit next to one another."""
    left_rc = get_rotated_tile(left, tiles_dict)[:, -1]
    right_lc = get_rotated_tile(right, tiles_dict)[:, 0]
    if all(left_rc == right_lc):
        return True
    return False


def tb_fit(top, bottom, tiles_dict):
    """Check whether both tiles fit on top of each other."""
    top_br = get_rotated_tile(top, tiles_dict)[-1, :]
    bottom_tr = get_rotated_tile(bottom, tiles_dict)[0, :]
    if all(top_br == bottom_tr):
        return True
    return False


def get_candidates(grid, tiles_left, location, tiles_dict):
    """Return a list with all candidates that fit in the specified location.

    Because we fill the grid from left to right and top to bottom, we only
    need to check whether the tiles fit with the left and top neighbours (unless
    they are on the first row or column."""
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
    return candidates


def solve(grid, tiles_left, size, tiles_dict):
    """Run an iteration to solve the grid.

    As long as there are tiles left to place, it tries each of them in any
    possible position (rotation and flip) until the remaining tiles in the new
    grid can also be solved."""
    if not tiles_left:
        return True
    location = get_next_empty(grid, size)
    potential_positions = get_candidates(grid, tiles_left, location, tiles_dict)
    while potential_positions:
        t = potential_positions.pop()
        grid[location] = t
        new_tiles_left = [ti for ti in tiles_left if t[0] != ti]
        result = solve(grid, new_tiles_left, size, tiles_dict)
        if result:
            return True
        else:
            grid[location] = None  # remove the tile that did not fit from the grid
    return False


def create_image(grid, side_length, tiles_dict):
    """Part 2 image from a given grid."""
    blocks = []
    for r in range(side_length):
        r_blocks = []
        for c in range(side_length):
            pos = grid[(r, c)]
            t = get_rotated_tile(pos, tiles_dict)
            t_strip = t[1:-1, 1:-1]
            r_blocks.append(t_strip)
        blocks.append(np.concatenate(r_blocks, axis=1))
    return np.concatenate(blocks, axis=0)


def count_sea(variation, sea_monster):
    """Find monsters and return empty sea water count."""
    monster_shape = sea_monster.shape
    variation_shape = variation.shape
    monster_space = np.sum(sea_monster)
    monsters_found = 0
    for r in range(variation_shape[0] - monster_shape[0]):
        for c in range(variation_shape[1] - monster_shape[1]):
            search_space = variation[r: r + monster_shape[0], c: c + monster_shape[1]]
            assert search_space.shape == monster_shape
            if np.sum(np.multiply(search_space, sea_monster)) == monster_space:
                print("found a monster! coords:", r, c)
                monsters_found += 1
    return np.sum(variation) - monsters_found * monster_space


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    tiles = list()
    for t, b in inp.items():
        body = [s.strip() for s in b.splitlines() if s.strip()]
        tiles.append(Tile(t, body))

    side_length = int(round(math.sqrt(len(tiles))))
    print(side_length)
    tiles_dict = {t.num: t for t in tiles}
    grid = {(r, c): None for r in range(side_length) for c in range(side_length)}
    tiles_left = [t.num for t in tiles]
    solution = solve(grid, tiles_left, side_length, tiles_dict)
    print(grid)
    p1 = (
            int(grid[0, 0][0])
            * int(grid[0, side_length - 1][0])
            * int(grid[side_length - 1, 0][0])
            * int(grid[side_length - 1, side_length - 1][0])
    )

    # part 2
    img = create_image(grid, side_length, tiles_dict)
    sea_monster = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        ]
    )
    print(img)
    print(img.shape)
    non_monsters = []
    for variation in get_rot_and_flip_variations(img):
        non_monsters.append(count_sea(variation, sea_monster))

    print("Non monsters", non_monsters)
    p2 = min(non_monsters)
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(20899048083289, p1)
    self.assertEqual(273, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    p1, p2 = main("full.txt")
    assert p1 == 107399567124539
    assert p2 == 1555
