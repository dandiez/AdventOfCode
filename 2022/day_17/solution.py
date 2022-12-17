from __future__ import annotations

import copy
import dataclasses
import itertools
from collections import defaultdict
from enum import Enum
from typing import Iterator, Iterable
from unittest import TestCase


class Material(Enum):
    air = 0
    rock = 1
    wall = 2
    floor = 3
    corner = 4

    def char(self):
        return CHAR_MAP[self]

    @property
    def is_solid(self):
        return self is not self.air


CHAR_MAP = {
    Material.air: ".",
    Material.rock: "█",
    Material.wall: "|",
    Material.floor: "-",
    Material.corner: "+"
}


@dataclasses.dataclass(frozen=True)
class Cell:
    material: Material


@dataclasses.dataclass
class CellBunch:
    _cells: dict[complex, Cell] = dataclasses.field(default_factory=dict)
    _offset: complex = 0

    def to_str(self, add_origin: complex |None=0):
        cop = copy.copy(self)
        if add_origin is not None:
            cop.add_more_cells(CellBunch({add_origin: Cell(Material.corner)}))
        s = []
        for y in range(cop.maxy, cop.miny - 1, -1):
            for x in range(cop.minx, cop.maxx + 1):
                pos = x + 1j * y
                if pos in cop:
                    s.append(cop[pos].material.char())
                else:
                    s.append(".")
            s.append("\n")
        return "".join(s)

    def __contains__(self, pos: complex):
        return pos - self._offset in self._cells

    def __getitem__(self, pos: complex):
        return self._cells[pos - self._offset]

    def __setitem__(self, key, value):
        self._cells[key - self._offset] = value

    def move_delta(self, delta: complex):
        self._offset += delta

    @property
    def w(self):
        return self.maxx - self.minx + 1

    @property
    def h(self):
        return self.maxy - self.miny + 1

    def __iter__(self) -> Iterable[complex, Cell]:
        yield from ((pos + self._offset, c) for pos, c in self._cells.items())

    @property
    def minx(self):
        return round(min(p.real for p, c in self))

    @property
    def miny(self):
        return round(min(p.imag for p, c in self))

    @property
    def maxx(self):
        return round(max(p.real for p, c in self))

    @property
    def maxy(self):
        return round(max(p.imag for p, c in self))

    def add_more_cells(self, other: CellBunch):
        self._cells.update((p - self._offset, c) for p, c in other)

    def clashes_with(self, other: CellBunch):
        if any(cpos in other for cpos, _ in self):
            return True
        return False

    def remove_pos(self, positions: set[complex]):
        for pos in positions:
            del self._cells[pos-self._offset]


@dataclasses.dataclass
class Rock(CellBunch):
    is_moving = True


BLOCKS = (
    Rock({pos: Cell(Material.rock) for pos in {0, 1, 2, 3}}),
    Rock({pos: Cell(Material.rock) for pos in {1, 1j, 1 + 1j, 2 + 1j, 1 + 2j}}),
    Rock({pos: Cell(Material.rock) for pos in {0, 1, 2, 2 + 1j, 2 + 2j}}),
    Rock({pos: Cell(Material.rock) for pos in {0, 1j, 2j, 3j}}),
    Rock({pos: Cell(Material.rock) for pos in {0, 1, 1j, 1 + 1j}}),
)


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return [1 if c == ">" else -1 for c in lines[0]]


@dataclasses.dataclass
class RockTrix(CellBunch):
    _rock_sequence: tuple[Rock, ...] = None
    _commands: list[complex] = None
    _left_wall_x = 0
    _right_wall_x = 8
    _appear_dy = 4
    _appear_dx = 3
    _rock_generator: Iterator[Rock] = None
    _command_generator: Iterator[complex] = None
    _command_id = 0
    _seen_positions: dict = dataclasses.field(default_factory=dict)
    _yoffset: int = 0

    def __post_init__(self):
        floor = CellBunch(_cells={p: Cell(Material.floor) for p in range(self._right_wall_x - self._left_wall_x)})
        floor[self._left_wall_x] = Cell(Material.corner)
        floor[self._right_wall_x] = Cell(Material.corner)
        self.add_more_cells(floor)
        self._rock_generator = (copy.deepcopy(r) for r in itertools.cycle(self._rock_sequence))
        self._command_generator = itertools.cycle(self._commands)


    def play_util_n_rocks_at_rest(self, target_rocks_at_rest: int):
        self.target_rocks_at_rest = target_rocks_at_rest
        self.passit = False
        self.rocks_at_rest = 0
        while self.rocks_at_rest < target_rocks_at_rest:
            #print(self.rocks_at_rest)
            #if self.passit:
            #    self.move_delta(self._yoffset)
            self.drop_one_rock()
            self.rocks_at_rest += 1
            self.simplify()

    def drop_one_rock(self):
        r = next(self._rock_generator)
        appear_pos = self._appear_dx + self._left_wall_x + 1j * (self._appear_dy + self.maxy_rocks)
        r.move_delta(appear_pos)
        self.grow_walls(r.maxy)
        r.is_moving = True
        while r.is_moving:
            self.try_push_rock(r)
            self.try_lower_rock(r)
        self.add_more_cells(r)

    def simplify(self):
        max_y_per_column = defaultdict(int)
        for pos, c in self:
            x, y = pos.real, pos.imag
            max_y_per_column[x] = max(y, max_y_per_column[x])
        to_remove = set()
        miny = min(max_y_per_column.values())
        for pos, c in self:
            x, y = pos.real, pos.imag
            if y < miny - 4:  # 4 magic constant based on trial and error (to avoid holes under ledges)
                to_remove.add(pos)
        self.remove_pos(to_remove)

    @property
    def maxy_rocks(self):
        try:
            return round(max(pos.imag for pos, c in self if c.material is Material.rock))
        except ValueError:
            return 0

    def try_push_rock(self, r: Rock):
        wind = next(self._command_generator)
        if self._command_id % len(self._commands) == 0 and not self.passit and not self._command_id==0:

            h = (self.to_str(self.miny*1j), r.to_str(self.miny*1j))
            print(h)
            if not h in self._seen_positions:
                self._seen_positions[h] = (self.rocks_at_rest, self.maxy)
            else:
                print(h)
                delta_rocks_at_rest = self.rocks_at_rest - self._seen_positions[h][0]
                delta_maxy = self.maxy - self._seen_positions[h][1]
                print(delta_rocks_at_rest, delta_maxy)
                reps = (self.target_rocks_at_rest-self.rocks_at_rest) // delta_rocks_at_rest
                self.rocks_at_rest += reps * delta_rocks_at_rest
                self._yoffset = reps * delta_maxy
                self.move_delta(self._yoffset*1j)
                r.move_delta(self._yoffset*1j)
                self.passit = True

        self._command_id += 1
        #    #self._seen_positions

        r.move_delta(wind)
        if r.clashes_with(self):
            r.move_delta(-wind)

    def try_lower_rock(self, r: Rock):
        gravity = -1j
        r.move_delta(gravity)
        if r.clashes_with(self):
            r.move_delta(-gravity)
            r.is_moving = False

    def grow_walls(self, maxy: int):
        current_top_y = self.maxy
        self.add_more_cells(
            CellBunch({self._left_wall_x + 1j * y: Cell(Material.wall) for y in range(current_top_y + 1, maxy + 1)}))
        self.add_more_cells(
            CellBunch({self._right_wall_x + 1j * y: Cell(Material.wall) for y in range(current_top_y + 1, maxy + 1)}))


def part_1(inp):
    game = RockTrix(_rock_sequence=BLOCKS, _commands=inp)
    game.play_util_n_rocks_at_rest(2022)
    return game.maxy_rocks


def part_2(inp):
    game = RockTrix(_rock_sequence=BLOCKS, _commands=inp)
    game.play_util_n_rocks_at_rest(1000000000000)
    return game.maxy_rocks


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")
    assert p1 == 3209
    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    inp = read_input("sample_1")
    self.assertEqual(3068, part_1(inp))
    print("part 1 test done.")


def test_sample_2(self):
    print("part 2 test...")
    inp = read_input("sample_1")
    self.assertEqual(1514285714288, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
