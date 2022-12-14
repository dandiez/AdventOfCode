import dataclasses
from enum import Enum
from unittest import TestCase
import numpy as np


def t2a(t: tuple) -> np.ndarray:
    """Get array from tuple."""
    return np.array(t)


def a2t(a: np.ndarray) -> tuple:
    """Round and cast array to int tuple."""
    return tuple(np.rint(a).astype(int))


class SimulationMustStop(Exception):
    """Raised if the simulation cannot continue."""


class InfiniteSandException(SimulationMustStop):
    """Sand goes into the void."""


class SandSourceStuckException(SimulationMustStop):
    """Sand reached the source."""


ROCK_BOTTOM_DELTA_Y = 2
PADDING = ROCK_BOTTOM_DELTA_Y


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    lines = [line.split("->") for line in lines]

    def raw_coord_to_tuple(raw_coord: str) -> tuple:
        a, b = raw_coord.split(",")
        return int(a), int(b)

    rock_segments = [
        [raw_coord_to_tuple(raw_coord) for raw_coord in line] for line in lines
    ]
    return rock_segments


class Material(Enum):
    air = 0
    rock = 1
    sand = 2
    sand_source = 3

    def char(self):
        return CHAR_MAP[self]

    @property
    def is_solid(self):
        return self is self.sand or self is self.rock


CHAR_MAP = {
    Material.air: " ",
    Material.rock: "█",
    Material.sand: "o",
    Material.sand_source: "+",
}

SAND_FALL_DIRS = (np.array((0, 1)), np.array((-1, 1)), np.array((1, 1)))


@dataclasses.dataclass
class Tile:
    pos: tuple
    material: Material
    is_at_rest: bool


@dataclasses.dataclass
class Cave:
    tiles: dict[tuple, Tile]
    _min_x: int = None
    _max_x: int = None
    _min_y: int = None
    _max_y: int = None

    def __str__(self):
        chars = []
        for y in range(self.min_y, self.max_y + 1 + PADDING):
            for x in range(self.min_x, self.max_x + 1):
                chars.append(self.mat_at_position((x, y)).char())
            chars.append("\n")
        return "".join(chars)

    def load_rocks(self, inp: list[list[tuple]]):
        for path in inp:
            for segment in zip(path, path[1:]):
                from_point, to_point = segment
                diff = t2a(to_point) - t2a(from_point)
                mag = np.linalg.norm(diff)
                unit = diff / mag
                for k in range(round(mag) + 1):
                    p = t2a(from_point) + k * unit
                    self.add_tile(
                        Tile(pos=a2t(p), material=Material.rock, is_at_rest=True)
                    )

    def add_tile(self, t: Tile):
        self.tiles[t.pos] = t

    def mat_at_position(self, pos: tuple):
        if pos not in self.tiles:
            return Material.air
        return self.tiles[pos].material

    def is_solid(self, pos: tuple) -> bool:
        return self.mat_at_position(pos).is_solid

    @property
    def min_x(self) -> int:
        if self._min_x is None:
            self._min_x = min(x for x, y in self.tiles)
        return self._min_x

    @property
    def max_x(self) -> int:
        if self._max_x is None:
            self._max_x = max(x for x, y in self.tiles)
        return self._max_x

    @property
    def min_y(self) -> int:
        if self._min_y is None:
            self._min_y = min(y for x, y in self.tiles)
        return self._min_y

    @property
    def max_y(self) -> int:
        if self._max_y is None:
            self._max_y = max(y for x, y in self.tiles)
        return self._max_y


@dataclasses.dataclass
class SandSimulator:
    cave: Cave
    source: tuple
    sand_landed: int = 0

    def __post_init__(self):
        """Add a source tile for display purposes."""
        source_tile = Tile(
            pos=self.source, material=Material.sand_source, is_at_rest=True
        )
        self.cave.add_tile(source_tile)

    def release_sand_block(self):
        t = Tile(self.source, material=Material.sand, is_at_rest=False)
        while not t.is_at_rest and not t.pos[1] > self.cave.max_y:
            self.move_sand(t)
        if not t.is_at_rest:
            raise InfiniteSandException(f"Sand escaped in position {t.pos}")
        self.cave.add_tile(t)
        self.sand_landed += 1

    def release_a_lot_of_sand(self):
        while True:
            try:
                self.release_sand_block()
            except SimulationMustStop:
                break

    def move_sand(self, t: Tile):
        for destination in self.get_destinations_just_below(t):
            if not self.cave.is_solid(destination):
                t.pos = destination
                return
        t.is_at_rest = True

    @staticmethod
    def get_destinations_just_below(t: Tile):
        p = t2a(t.pos)
        for dir in SAND_FALL_DIRS:
            destination = p + dir
            yield a2t(destination)


@dataclasses.dataclass
class SandSimulator2(SandSimulator):
    def release_sand_block(self):
        t = Tile(self.source, material=Material.sand, is_at_rest=False)
        while not t.is_at_rest and not t.pos[1] > self.cave.max_y + ROCK_BOTTOM_DELTA_Y:
            self.expand_rock_bottom(t)
            self.move_sand(t)
        if not t.is_at_rest:
            raise InfiniteSandException(f"Sand escaped in position {t.pos}")
        self.cave.add_tile(t)
        self.sand_landed += 1
        if t.pos == self.source:
            raise SandSourceStuckException()

    def expand_rock_bottom(self, t: Tile):
        one_to_rock_bottom = self.cave.max_y + ROCK_BOTTOM_DELTA_Y - 1
        if not t.pos[1] == one_to_rock_bottom:
            return
        for pos in self.get_destinations_just_below(t):
            self.cave.add_tile(Tile(pos=pos, material=Material.rock, is_at_rest=True))


def part_1(inp):
    c = Cave(dict())
    c.load_rocks(inp)
    s = SandSimulator(cave=c, source=(500, 0))
    s.release_a_lot_of_sand()
    print(c)
    return s.sand_landed


def part_2(inp):
    c = Cave(dict())
    c.load_rocks(inp)
    s = SandSimulator2(cave=c, source=(500, 0))
    s.release_a_lot_of_sand()
    print(c)
    return s.sand_landed


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
    self.assertEqual(24, part_1(inp))


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(93, part_2(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
