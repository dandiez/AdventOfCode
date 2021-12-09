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
    yield from (val + 1 for coords, val in find_local_min_values(grid))


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
                yield (i, j), val


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
    grid = get_grid(inp)
    basins = get_basins(grid)
    sizes = get_basin_sizes(basins)
    sizes_sorted = sorted(list(sizes))
    return sizes_sorted[-1] * sizes_sorted[-2] * sizes_sorted[-3]


def get_basin_sizes(basins):
    for basin in basins:
        yield len(basin)


def get_basins(grid):
    basins = []
    starting_points = set(coords for coords, val in find_local_min_values(grid))
    while starting_points:
        point = starting_points.pop()
        basins.append(find_basin_around_point(point, grid))
    return basins


def find_basin_around_point(point, grid):
    basin_points = {point}
    neigh = set(neighbours(*point))
    seen = set.union(basin_points, neigh)
    while neigh:
        n = neigh.pop()
        seen.add(n)
        if n not in grid.grid:
            continue
        if grid.grid[n] == 9:
            continue
        more_neigh = set(nn for nn in neighbours(*n) if nn not in seen)
        neigh.update(more_neigh)
        basin_points.add(n)
    return basin_points


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
    self.assertEqual(1134, part_2(inp))


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    print('*** solving main ***')
    main("input")
