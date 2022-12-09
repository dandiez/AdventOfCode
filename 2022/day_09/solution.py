import dataclasses
from unittest import TestCase

import numpy as np

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
        self.H = self.H + dir
        self.catch_up()
        self.t_visited.add(tuple(self.T))

    def catch_up(self):
        delta = self.H - self.T
        dx = delta * np.array([1, 0])
        dy = delta * np.array([0, 1])
        if abs(dx)[0]==2 and abs(dy)[1]==0:
            self.T += dx // 2
        elif abs(dy)[1]==2 and abs(dx)[0] == 0:
            self.T += dy // 2
        elif abs(dx)[0]==2 and abs(dy)[1] == 1:
            self.T += dx // 2 +dy
        elif abs(dy)[1]==2 and abs(dx)[0] == 1:
            self.T += dy // 2 + dx

def part_1(inp):
    ht = HT(
    H = np.array([0,0]),
    T = np.array([0,0]), t_visited=set())
    for dir, count in inp:
        for _ in range(count):
            ht.move(dir)
    return len(ht.t_visited)



def part_2(inp):
    pass


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
    pass


def test_sample_2(self):
    # inp = read_input("sample_1")
    # self.assertEqual(1, part_1(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
