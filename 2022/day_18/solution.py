import dataclasses
from unittest import TestCase

import networkx as nx
import numpy as np


def get_six_directions():
    pos_units = [np.array([1, 0, 0]), np.array([0, -1, 0]), np.array([0, 0, -1])]
    neg_units = [-a for a in pos_units]
    yield from pos_units
    yield from neg_units


@dataclasses.dataclass(frozen=True)
class Point:
    coords: tuple[int, int, int]

    @classmethod
    def from_string(cls, s: str):
        return cls(tuple([int(n) for n in s.split(",")]))

    def neighbours(self):
        center = np.array(self.coords)
        for d in get_six_directions():
            yield Point(tuple(center + d))


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    inp = [Point.from_string(val) for val in lines]  # parse here...
    return inp


def part_1(inp):
    all_points = set(inp)
    return sum(n not in all_points for p in all_points for n in p.neighbours())


def part_2(inp):
    lava = set(inp)
    air = set(n for p in lava for n in p.neighbours() if n not in lava)
    more_air = set(n for p in air for n in p.neighbours() if n not in lava)
    air.update(more_air)

    G = nx.Graph()
    for p in lava:
        G.add_node(p)
    for p in air:
        G.add_node(p)
    for n in G.nodes:
        for nei in n.neighbours():
            if nei in air or nei in lava:
                G.add_edge(n, nei)

    max_x = max(p.coords[0] for p in air)
    outside_air = next(p for p in air if p.coords[0] == max_x)

    for n in lava:
        G.remove_node(n)

    air_outside = set(n for n in air if nx.has_path(G, outside_air, n))
    return sum(n not in lava for p in lava for n in p.neighbours() if n in air_outside)


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


def test_sample_1(self):
    inp = read_input("sample_1")
    self.assertEqual(64, part_1(inp))


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(58, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
