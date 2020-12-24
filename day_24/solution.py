from unittest import TestCase

import lark
import numpy as np


def read_input(filename="input.txt"):
    with open(filename) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    grammar = r"""
        start: direction (direction)*
        direction: "ne" -> ne
            | "nw" -> nw
            | "se" -> se
            | "sw" -> sw
            | "e" -> e
            | "w" -> w
        _NEWLINE: "\n"
        %import common.WS
        %ignore WS
    """

    class TransformPaths(lark.Transformer):
        start = list
        path = list
        se = lambda self, items: np.array((1, -1))
        sw = lambda self, items: np.array((0, -1))
        ne = lambda self, items: np.array((0, 1))
        nw = lambda self, items: np.array((-1, 1))
        w = lambda self, items: np.array((-1, 0))
        e = lambda self, items: np.array((1, 0))

    parser = lark.Lark(grammar)
    data = []
    for line in lines:
        p = parser.parse(line)
        # print(p.pretty())
        d = TransformPaths().transform(p)
        # print(d)
        data.append(d)
    return data


import functools


@functools.lru_cache(None)
def get_neighbours(tile):
    tile = np.array(tile)
    deltas = [np.array((1, -1)), np.array((0, -1)),
              np.array((0, 1)), np.array((-1, 1))
        , np.array((-1, 0))
        , np.array((1, 0))]
    return {tuple(tile + d) for d in deltas}


def run_iteration(tiles):
    new_tiles = set()
    all_tiles = set()
    for t in tiles:
        n = get_neighbours(t)
        all_tiles = all_tiles.union(n)

    for t in all_tiles:
        n = get_neighbours(t)
        number_of_black_neighbours = len(tiles.intersection(n))
        if t in tiles:
            # is black
            if (number_of_black_neighbours == 0 or number_of_black_neighbours > 2):
                pass
            else:
                new_tiles.add(t)
        else:
            # is white
            if number_of_black_neighbours == 2:
                new_tiles.add(t)
    return new_tiles


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    data = read_input(input_file)
    # print(f"Data contains {len(data)} paths")
    tiles = []
    for p in data:
        tile = tuple(sum(p))
        if tile in tiles:
            tiles.remove(tile)
            # print(f"tile {tile} was there already. flipping it back.")
        else:
            tiles.append(tile)
            # print(f"flipped tile {tile}")

    p1 = len(tiles)
    # part 2
    tiles = set(tiles)
    for day in range(1, 100 + 1):
        tiles = run_iteration(tiles)
        p2 = len(tiles)
        print(f"Day {day}: {p2}")

    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_samples(self):
    input_file = "sample_1.txt"
    p1, p2 = main(input_file)
    self.assertEqual(10, p1)
    self.assertEqual(2208, p2)
    print("***Tests passed so far***")


if __name__ == "__main__":
    test_samples(TestCase())
    main("full.txt")
