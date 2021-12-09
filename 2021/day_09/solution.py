import dataclasses
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[int(val) for val in line] for line in lines]  # parse here...
    return inp


def part_1(inp):
    grid = get_grid(inp)
    return sum(get_risk_levels(grid))


@dataclasses.dataclass
class Grid:
    num_rows: int
    num_cols: int
    grid: dict


def get_risk_levels(grid: Grid):
    yield from (val + 1 for val in find_local_min_values(grid))


def get_grid(inp):
    grid = dict()
    num_rows = len(inp)
    num_cols = len(inp[0])
    for i, row in enumerate(inp):
        for j, val in enumerate(row):
            grid[i, j] = val
    return Grid(num_rows=num_rows, num_cols=num_cols, grid=grid)


def find_local_min_values(grid: Grid):
    for i in range(grid.num_rows):
        for j in range(grid.num_cols):
            val = grid.grid[i, j]
            if is_min((i, j), grid):
                print(f'min in {i,j}:{val}')
                yield val


def is_min(coords, grid: Grid):
    val = grid.grid[coords]
    for neighbour in neighbours(*coords):
        if neighbour not in grid.grid:
            continue
        if grid.grid[neighbour] <= val:
            return False
    return True


def neighbours(i, j):
    for n in [i - 1, i + 1]:
        yield n, j
    for m in [j - 1, j + 1]:
        yield i, m


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
    self.assertEqual(15, part_1(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
