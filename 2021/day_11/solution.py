import dataclasses
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[int(val) for val in line] for line in lines]  # parse here...
    return inp


@dataclasses.dataclass
class Grid:
    num_rows: int
    num_cols: int
    grid: dict
    neighbours: dict = dataclasses.field(init=False)

    def __post_init__(self):
        self._calculate_all_valid_neighbours()

    def _calculate_all_valid_neighbours(self):
        self.neighbours = dict()
        for location in self.grid:
            self.neighbours[location] = self._calculate_valid_neighbours_at_location(
                location
            )

    def _calculate_valid_neighbours_at_location(self, location):
        neighbours = []
        i, j = location
        for n in range(i - 1, i + 2):
            for m in range(j - 1, j + 2):
                if (n, m) != (i, j) and (n, m) in self.grid:
                    neighbours.append((n, m))
        return tuple(neighbours)


def get_grid(inp):
    num_rows = len(inp)
    num_cols = len(inp[0])
    grid = {(i, j): val for i, row in enumerate(inp) for j, val in enumerate(row)}
    return Grid(num_rows=num_rows, num_cols=num_cols, grid=grid)


def part_1(inp):
    g = get_grid(inp)
    return sum(simulate_step(g) for _ in range(100))

def part_2(inp):
    g = get_grid(inp)
    for n in range(1, 99999999):
        try:
            simulate_step(g)
        except StopIteration:
            return n


def simulate_step(g):
    increment_all(g.grid)
    already_flashed = set()
    while True:
        new_flashers = {
            loc for loc in needs_flashing(g.grid) if loc not in already_flashed
        }
        if not new_flashers:
            break
        while new_flashers:
            loc = new_flashers.pop()
            flash_neighbours(g, loc)
            already_flashed.add(loc)
    num_flashed = count_and_reset_flashed(g.grid)
    if len(already_flashed) == len(g.grid):
        raise StopIteration('in sync')
    return num_flashed


def increment_all(grid):
    for loc in grid:
        grid[loc] += 1


def needs_flashing(grid):
    return set(loc for loc in grid if grid[loc] > 9)


def flash_neighbours(g: Grid, loc):
    neighbours = g.neighbours[loc]
    for n in neighbours:
        g.grid[n] += 1


def count_and_reset_flashed(grid):
    count = 0
    for loc in grid:
        if grid[loc] > 9:
            grid[loc] = 0
            count += 1
    return count




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
    self.assertEqual(1656, part_1(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
