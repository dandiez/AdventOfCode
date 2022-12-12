import dataclasses
from typing import Iterable
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


@dataclasses.dataclass
class Cell:
    coords: tuple
    height: int
    is_start: bool = False
    is_end: bool = False
    visited: bool = False
    distance_to_start: int = None


def get_height(c: str):
    return ord(c) - ord("a")


@dataclasses.dataclass
class Hill:
    _cells: dict[tuple, Cell]
    start_cell: Cell = None
    end_cell: Cell = None

    def __post_init__(self):
        self.start_cell = next(c for c in self._cells.values() if c.is_start)
        self.end_cell = next(c for c in self._cells.values() if c.is_end)

    @classmethod
    def from_raw(cls, lines: list[str]):
        cells = dict()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                is_start = False
                is_end = False
                if c == "S":
                    height = get_height("a")
                    is_start = True
                elif c == "E":
                    height = get_height("z")
                    is_end = True
                else:
                    height = get_height(c)
                cells[(x, y)] = Cell(coords=(x, y), height=height, is_start=is_start,
                                     is_end=is_end)
        return cls(cells)

    def find_top(self):
        self.start_cell.distance_to_start = 0
        next_to_visit = {self.start_cell.coords}
        while self.end_cell.visited is not True:
            candidates = set(c for c in self.find_candidates(next_to_visit))
            next_to_visit = candidates

    def find_candidates(self, next_to_visit: set[tuple]) -> Iterable[Cell]:
        cells_to_visit = (self._cells[pos] for pos in next_to_visit)
        for c in cells_to_visit:
            yield from self.visit(c)

    def visit(self, c: Cell) -> Iterable[tuple]:
        c.visited = True
        for neighbour in self.get_neighbours(c):
            if not neighbour.visited and (neighbour.height - c.height) <= 1:
                neighbour.distance_to_start = c.distance_to_start + 1
                yield neighbour.coords

    def get_neighbours(self, c: Cell) -> Iterable[Cell]:
        x, y = c.coords
        for pos in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if pos in self._cells:
                yield self._cells[pos]


def part_1(inp):
    h = Hill.from_raw(inp)
    h.find_top()
    return h.end_cell.distance_to_start


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
    self.assertEqual(31, part_1(inp))
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
