import dataclasses
from collections import defaultdict
from enum import Enum
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


class Direction(Enum):
    W = 0
    S = 1


Location = tuple[int, int]


@dataclasses.dataclass
class SeaFloor:
    cucus: dict[Direction, set[Location]]
    step: int = 1
    min_r: int = 0
    max_r: int = 0
    min_c: int = 0
    max_c: int = 0
    no_more_moves: bool = False

    def __post_init__(self):
        self.max_r = max(r for r, c in self.yield_all_cucus())
        self.max_c = max(c for r, c in self.yield_all_cucus())

    def yield_all_cucus(self):
        for direction, herd in self.cucus.items():
            for cucu in herd:
                yield cucu

    def solve(self):
        while self.no_more_moves is False:
            self.run_step()
        return self.step

    def run_step(self):
        new_cucus = defaultdict(set)
        at_least_one_moved = False
        for direction in [Direction.W, Direction.S]:
            for cucu in self.cucus[direction]:
                neighbour = self.get_neighbour(cucu, direction)
                if self.location_is_free(neighbour):
                    at_least_one_moved = True
                    new_cucus[direction].add(neighbour)
                else:
                    new_cucus[direction].add(cucu)
            self.cucus[direction] = new_cucus[direction]
        if at_least_one_moved:
            self.step += 1
        else:
            self.no_more_moves = True

    def location_is_free(self, location: Location):
        for direction, herd in self.cucus.items():
            if location in herd:
                return False
        return True

    def get_neighbour(self, cucu: Location, direction: Direction):
        if direction is Direction.W:
            return self.space_west(cucu)
        return self.space_south(cucu)

    def space_west(self, cucu: Location):
        r, c = cucu
        if c == self.max_c:
            return r, 0
        return r, c + 1

    def space_south(self, cucu: Location):
        r, c = cucu
        if r == self.max_r:
            return 0, c
        return r + 1, c

    @classmethod
    def load_from_inp(cls, inp: list[str]):
        cucus = defaultdict(set)
        for r, row in enumerate(inp):
            for c, value in enumerate(row):
                if value == ">":
                    cucus[Direction.W].add((r, c))
                elif value == "v":
                    cucus[Direction.S].add((r, c))
        return cls(cucus=cucus)


def part_1(inp):
    sea = SeaFloor.load_from_inp(inp)
    return sea.solve()


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
    sea = SeaFloor.load_from_inp(inp)
    self.assertEqual(58, sea.solve())


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
