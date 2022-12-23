from __future__ import annotations

import dataclasses
import itertools
from collections import defaultdict
from enum import Enum
from typing import Iterator
from unittest import TestCase

r = round

N = 1j
S = -N
E = 1
W = -E
NE = N + E
NW = N + W
SE = S + E
SW = S + W
ALL_DIRS = {N, S, E, W, NE, NW, SE, SW}


@dataclasses.dataclass(frozen=True)
class DirCheck:
    dirs_to_check: tuple[complex, complex, complex]
    dir_to_move_to: complex


Dir_Rotation = [
    DirCheck((N, NE, NW), N),
    DirCheck((S, SE, SW), S),
    DirCheck((W, NW, SW), W),
    DirCheck((E, NE, SE), E),
]


class Mat(Enum):
    ground = 0
    elf = 1

    @classmethod
    def from_char(cls, char: str):
        match char:
            case "#":
                return Mat.elf
            case ".":
                return Mat.ground
            case _:
                raise ValueError(f"Bad {char=}")

    def char(self):
        return CHAR_MAP[self]


CHAR_MAP = {
    Mat.ground: ".",
    Mat.elf: "█",
}


@dataclasses.dataclass
class Elf:
    material: Mat
    target_loc: complex = None


@dataclasses.dataclass
class Grove:
    elves: dict[complex, Elf]
    min_coords: complex
    max_coords: complex
    dir_generator: Iterator = None

    def __post_init__(self):
        self.dir_generator = itertools.cycle(Dir_Rotation)

    @classmethod
    def from_input(cls, s: str):
        lines = [l.strip() for l in s.splitlines() if l.strip()]
        min_x = 0
        min_y = 0
        max_x = len(lines)
        max_y = max(len(line) for line in lines) - 1
        cells = dict()
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x):
                char = lines[max_y - y][x]
                mat = Mat.from_char(char)
                if mat is not Mat.elf:
                    continue
                coords = x + 1j * y
                cells[coords] = Elf(material=mat)
        return cls(
            elves=cells, min_coords=min_x + 1j * min_y, max_coords=max_x + 1j * max_y
        )

    def show(self):
        PAD = 2
        s = []
        for y in range(
            r(self.max_coords.imag) + PAD, r(self.min_coords.imag) - 1 - PAD, -1
        ):
            for x in range(
                r(self.min_coords.real) - PAD, r(self.max_coords.real) + PAD
            ):
                cell_coords = x + 1j * y
                if cell_coords == 0:
                    s.append("x")
                elif cell_coords not in self.elves:
                    s.append(Mat.ground.char())
                else:
                    s.append(self.elves[cell_coords].material.char())
            s.append("\n")
        print("".join(s))

    def split_up(self, number_of_rounds=10):
        for _ in range(number_of_rounds):
            self.split_up_one_round()
            next(self.dir_generator)

    def split_up_one_round(self):
        proposed = self.phase_1()
        self.phase_2(proposed)
        self.update_ranges()

    def phase_1(self) -> dict[int]:
        self.clear_elf_targets()
        proposed = defaultdict(int)
        for _ in range(4):
            dirs: DirCheck = next(self.dir_generator)
            for loc, e in self.elves.items():
                if self.is_alone(loc):
                    continue
                if e.target_loc is not None:
                    continue
                adj = [loc + p for p in dirs.dirs_to_check]
                if all(a not in self.elves for a in adj):
                    target = loc + dirs.dir_to_move_to
                    proposed[target] += 1
                    self.elves[loc].target_loc = target
        return proposed

    def is_alone(self, loc: complex):
        for d in ALL_DIRS:
            if loc + d in self.elves:
                return False
        return True

    def clear_elf_targets(self):
        for e in self.elves.values():
            e.target_loc = None

    def phase_2(self, proposed):
        to_move = []
        for loc, e in self.elves.items():
            if e.target_loc is None:
                continue
            elif proposed[e.target_loc] != 1:
                continue
            else:
                to_move.append((loc, e))
        for loc, e in to_move:
            del self.elves[loc]
            self.elves[e.target_loc] = e

    def update_ranges(self):
        x = {loc.real for loc in self.elves}
        y = {loc.imag for loc in self.elves}
        self.min_coords = min(x) + 1j * min(y)
        self.max_coords = max(x) + 1j * max(y)
        return

    def count_ground_cells(self):
        delta = self.max_coords - self.min_coords
        total = (delta.real + 1) * (delta.imag + 1)
        return total - len(self.elves)


def part_1(inp):
    g = Grove.from_input(inp)
    g.split_up(10)
    return g.count_ground_cells()


def part_2(inp):
    pass


def read_input(filename="input"):
    with open(filename) as f:
        return f.read()


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
    self.assertEqual(110, part_1(inp))


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
