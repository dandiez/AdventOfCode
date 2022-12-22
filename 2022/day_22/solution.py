from __future__ import annotations
import dataclasses
from enum import Enum
from typing import Literal, Iterable
from typing import TypeAlias
from unittest import TestCase
import re

RIGHT = complex(0, 1)
LEFT = complex(0, -1)
UP = complex(-1, 0)
DOWN = complex(1, 0)
DIRS = (RIGHT, DOWN, LEFT, UP)
DIR_TO_SCORE = {d: s for s, d in enumerate(DIRS)}
ROTATIONS = {"R": -1j, "L": 1j}

Location: TypeAlias = complex
Dir: TypeAlias = complex  # one of [RIGHT, DOWN, LEFT, UP]
Instruction = int | Literal["R", "L"]


class WallOnTheWay(Exception):
    """Cannot move. Wall is on the way."""


class Mat(Enum):
    air = 0
    wall = 1

    @classmethod
    def from_char(cls, char: str):
        match char:
            case "#":
                return Mat.wall
            case ".":
                return Mat.air
            case _:
                raise ValueError(f"Bad {char=}")

    def char(self):
        return CHAR_MAP[self]


CHAR_MAP = {
    Mat.air: ".",
    Mat.wall: "█",
    RIGHT: ">",
    LEFT: "<",
    UP: "^",
    DOWN: "v",
}


@dataclasses.dataclass
class Cell:
    coords: complex
    material: Mat
    neighbours: dict[Dir, Cell] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Agent:
    facing: Dir
    location: Cell = None

    def rotate(self, r: Literal["R", "L"]):
        self.facing *= ROTATIONS[r]


@dataclasses.dataclass
class Board:
    agent: Agent
    cells: dict[complex, Cell]
    instructions: list[Instruction]
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    start: Cell = None

    def __post_init__(self):

        self.connect_cells()
        self.set_start()
        self.agent.location = self.start

    @classmethod
    def from_inp(cls, inp: str):
        map, instr = inp.split("\n\n")[:2]
        instructions = [v.strip() for v in re.split("(\d+)", instr) if v.strip()]
        instructions = [v if v in ROTATIONS else int(v) for v in instructions]
        lines = map.split("\n")
        min_x = 1
        min_y = 1
        max_x = len(lines)
        max_y = max(len(line) for line in lines)
        return cls(
            agent=Agent(facing=RIGHT),
            cells={
                c.coords: c
                for c in cls.cells_from_str(lines, min_x, max_x, min_y, max_y)
            },
            instructions=instructions,
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
        )

    @classmethod
    def cells_from_str(
        cls, lines: list[str], min_x, max_x, min_y, max_y
    ) -> Iterable[Cell]:
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                try:
                    c = lines[x - 1][y - 1]
                except IndexError:
                    continue
                if c == " ":
                    continue
                yield Cell(coords=x + 1j * y, material=Mat.from_char(c))

    def connect_cells(self):
        for c in self.cells.values():
            for d in DIRS:
                neighbour_loc = c.coords + d
                if neighbour_loc not in self.cells:
                    neighbour_loc = c.coords
                    search_dir = -d
                    while neighbour_loc in self.cells:
                        neighbour_loc += search_dir
                    neighbour_loc -= search_dir
                c.neighbours[d] = self.cells[neighbour_loc]

    def set_start(self):
        ymin = 9e999
        for c in self.cells:
            if c.real == self.min_x:
                ymin = min(ymin, c.imag)
        self.start = self.cells[self.min_x + 1j * ymin]

    def get_final_password(self):
        a_coords = self.agent.location.coords
        return (
            a_coords.real * 1000 + a_coords.imag * 4 + DIR_TO_SCORE[self.agent.facing]
        )

    def run_instructions(self):
        for i in self.instructions:
            if i in ROTATIONS:
                self.agent.rotate(i)
            else:
                self.move_agent(i)
            #  print(self)

    def move_agent(self, n: int):
        for _ in range(n):
            try:
                self.move_agent_one()
            except WallOnTheWay:
                return

    def move_agent_one(self):
        a_loc = self.agent.location
        destination = a_loc.neighbours[self.agent.facing]
        if destination.material is Mat.wall:
            raise WallOnTheWay()
        else:
            self.agent.location = destination

    def __str__(self):
        chars = []
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                coords = x + 1j * y
                if self.agent.location.coords == coords:
                    chars.append(CHAR_MAP[self.agent.facing])
                    continue
                if coords not in self.cells:
                    chars.append(" ")
                else:
                    chars.append(self.cells[coords].material.char())
            chars.append("\n")
        return "".join(chars)


def read_input(filename="input"):
    with open(filename) as f:
        return f.read()


def part_1(inp):
    b = Board.from_inp(inp)
    b.run_instructions()
    return b.get_final_password()


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
    self.assertEqual(6032, part_1(inp))


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
