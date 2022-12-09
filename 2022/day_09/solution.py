import dataclasses
from unittest import TestCase

import numpy as np


def magnitude(a: np.ndarray):
    """Get vector magnitude."""
    return np.linalg.norm(a)


def unitv(v: np.ndarray):
    """Get the unit vector (as int)."""
    m = magnitude(v)
    if m == 0:
        return v
    return (v // m).astype(int)


DIRS = {
    "U": np.array([0, 1]),
    "D": np.array([0, -1]),
    "L": np.array([-1, 0]),
    "R": np.array([1, 0]),
}


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [val.split() for val in lines]  # parse here...
    inp = [(DIRS[a], int(b)) for a, b in inp]
    return inp


@dataclasses.dataclass
class Link:
    H: np.ndarray
    T: np.ndarray
    t_visited: set[tuple[int, int]]

    def move(self, direction: np.ndarray):
        if tuple(direction) == (0, 0):
            return
        self.H = self.H + direction
        self.catch_up()
        self.t_visited.add(tuple(self.T))

    def catch_up(self):
        delta = self.H - self.T
        dx = delta * np.array([1, 0])
        dy = delta * np.array([0, 1])
        maxmov = max(magnitude(dx), magnitude(dy))
        if maxmov == 2:
            self.T += unitv(dx) + unitv(dy)
        return


@dataclasses.dataclass
class Chain:
    links: list[Link]

    def move(self, direction: np.ndarray):
        self.links[0].move(direction)
        for n in range(1, len(self.links)):
            new_dir = self.links[n - 1].T - self.links[n].H
            self.links[n].move(new_dir)


def part_1(inp):
    ht = Link(H=np.array([0, 0]), T=np.array([0, 0]), t_visited=set())
    for dir, count in inp:
        for _ in range(count):
            ht.move(dir)
    return len(ht.t_visited)


def part_2(inp):
    chain = Chain(
        [
            Link(H=np.array([0, 0]), T=np.array([0, 0]), t_visited={(0, 0)})
            for _ in range(9)
        ]
    )
    for dir, count in inp:
        for _ in range(count):
            chain.move(dir)
    return len(chain.links[-1].t_visited)


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
    self.assertEqual(13, part_1(inp))


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(1, part_2(inp))
    inp = read_input("sample_2")
    self.assertEqual(36, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
