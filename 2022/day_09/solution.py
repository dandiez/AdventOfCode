import dataclasses
from unittest import TestCase

import numpy as np


def mod(a: np.ndarray):
    return np.linalg.norm(a)


DIRS = {"U": np.array([0, 1]),
        "D": np.array([0, -1]),
        "L": np.array([-1, 0]),
        "R": np.array([1, 0])}


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [val.split() for val in lines]  # parse here...
    inp = [(DIRS[a], int(b)) for a, b in inp]
    return inp


@dataclasses.dataclass
class HT:
    H: np.ndarray
    T: np.ndarray
    t_visited: set[tuple[int, int]]

    def move(self, dir: np.ndarray):
        if tuple(dir) == (0, 0):
            return
        self.H = self.H + dir
        self.catch_up()
        self.t_visited.add(tuple(self.T))

    def catch_up(self):
        delta = self.H - self.T
        if tuple(delta) == (0, 0):
            return
        dx = delta * np.array([1, 0])
        dy = delta * np.array([0, 1])
        if mod(dx) == 2 and mod(dy) == 0:
            self.T += dx // 2
        elif mod(dy) == 2 and mod(dx) == 0:
            self.T += dy // 2
        elif mod(dx) == 2 and mod(dy) == 1:
            self.T += dx // 2 + dy
        elif mod(dy) == 2 and mod(dx) == 1:
            self.T += dy // 2 + dx
        elif mod(dy) == 2 and mod(dx) == 2:
            self.T += dy // 2 + dx // 2
        elif mod(dx) == 1 or mod(dy) == 1:
            return
        else:
            raise ValueError(delta)


@dataclasses.dataclass
class Chain:
    links: list[HT]

    def move(self, dir: np.ndarray):
        self.links[0].move(dir)
        for n in range(1, len(self.links)):
            new_dir = self.links[n - 1].T - self.links[n].H
            self.links[n].move(new_dir)


def part_1(inp):
    ht = HT(
        H=np.array([0, 0]),
        T=np.array([0, 0]), t_visited=set()
    )
    for dir, count in inp:
        for _ in range(count):
            ht.move(dir)
    return len(ht.t_visited)


def part_2(inp):
    chain = Chain([HT(
        H=np.array([0, 0]),
        T=np.array([0, 0]), t_visited={(0, 0)}
    ) for _ in range(10)])
    for dir, count in inp:
        for _ in range(count):
            chain.move(dir)
    return len(chain.links[-2].t_visited)


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
