import dataclasses
from unittest import TestCase

from parse import parse


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [
        parse("{state} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line) for line in lines
    ]  # parse here...
    return inp


@dataclasses.dataclass(frozen=True)
class Cube:
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def coords(self):
        return [self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax]

    def x_coords(self):
        return [self.xmin, self.xmax]

    def y_coords(self):
        return [self.ymin, self.ymax]

    def z_coords(self):
        return [self.zmin, self.zmax]

    def is_valid(self):
        x_ok = self.xmin <= self.xmax
        y_ok = self.ymin <= self.ymax
        z_ok = self.zmin <= self.zmax
        return x_ok and y_ok and z_ok

    def vertices(self):
        for x in (self.xmin, self.xmax):
            for y in (self.ymin, self.ymax):
                for z in (self.zmin, self.zmax):
                    yield x, y, z

    def split(self, vertex):
        if not self.contains(vertex):
            return self
        x, y, z = vertex
        return [
            Cube(self.xmin, x, self.ymin, y, self.zmin, z),
            Cube(x, self.xmax, self.ymin, y, self.zmin, z),
            Cube(self.xmin, x, y, self.ymax, self.zmin, z),
            Cube(x, self.xmax, y, self.ymax, self.zmin, z),
            Cube(self.xmin, x, self.ymin, y, z, self.zmax),
            Cube(x, self.xmax, self.ymin, y, z, self.zmax),
            Cube(self.xmin, x, y, self.ymax, z, self.zmax),
            Cube(x, self.xmax, y, self.ymax, z, self.zmax),
        ]

    def contains(self, vertex):
        x, y, z = vertex
        x_in = self.xmin <= x <= self.xmax
        y_in = self.ymin <= y <= self.ymax
        z_in = self.zmin <= z <= self.zmax
        return x_in and y_in and z_in

    def contained_in_cube(self, cube):
        for vertex in self.vertices():
            if not cube.contains(vertex):
                return False
        return True

    def split_x(self, x):
        if not self.xmin <= x <= self.xmax:
            return {self}
        lower = Cube(self.xmin, x - 1, self.ymin, self.ymax, self.zmin, self.zmax)
        mid = Cube(x, x, self.ymin, self.ymax, self.zmin, self.zmax)
        upper = Cube(x + 1, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)
        return {cube for cube in [lower, mid, upper] if cube.is_valid()}

    def split_y(self, y):
        if not self.ymin <= y <= self.ymax:
            return {self}
        lower = Cube(self.xmin, self.xmax, self.ymin, y - 1, self.zmin, self.zmax)
        mid = Cube(self.xmin, self.xmax, y, y, self.zmin, self.zmax)
        upper = Cube(self.xmin, self.xmax, y + 1, self.ymax, self.zmin, self.zmax)
        return {cube for cube in [lower, mid, upper] if cube.is_valid()}

    def split_z(self, z):
        if not self.zmin <= z <= self.zmax:
            return {self}
        lower = Cube(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, z - 1)
        mid = Cube(self.xmin, self.xmax, self.ymin, self.ymax, z, z)
        upper = Cube(self.xmin, self.xmax, self.ymin, self.ymax, z + 1, self.zmax)
        return {cube for cube in [lower, mid, upper] if cube.is_valid()}

    def do_not_overlap_for_sure(self, other):
        x_higher = other.xmin > self.xmax
        x_lower = other.xmax < self.xmin
        x_clear = x_higher or x_lower
        if x_clear:
            return True
        y_higher = other.ymin > self.ymax
        y_lower = other.ymax < self.ymin
        y_clear = y_higher or y_lower
        if y_clear:
            return True
        z_higher = other.zmin > self.zmax
        z_lower = other.zmax < self.zmin
        z_clear = z_higher or z_lower
        return z_clear

    def count(self):
        return (
            (self.xmax - self.xmin + 1)
            * (self.ymax - self.ymin + 1)
            * (self.zmax - self.zmin + 1)
        )


@dataclasses.dataclass
class Operation:
    cube: Cube
    state: bool


@dataclasses.dataclass
class Space:
    regions: set[Cube]

    def apply_operation(self, operation: Operation):
        print(operation, len(self.regions), sum(c.count() for c in self.regions))
        cube = operation.cube

        self.regions = Space.split_by_cube(self.regions, cube)
        subcubes = Space.split_by_many_cubes({cube}, self.regions)
        if operation.state is True:
            self.regions.update(subcubes)
        else:
            self.regions.difference_update(subcubes)

    @staticmethod
    def split_by_many_cubes(regions: set[Cube], cubes: set[Cube]):
        for cube in cubes:
            regions = Space.split_by_cube(regions, cube)
        return regions

    @staticmethod
    def split_by_cube(regions: set[Cube], cube: Cube):
        regions_to_split = set()
        regions_to_keep = set()
        while regions:
            r = regions.pop()
            if r.do_not_overlap_for_sure(cube):
                regions_to_keep.add(r)
            else:
                regions_to_split.add(r)

        regions = regions_to_split
        for x in cube.x_coords():
            regions = Space.split_at_x(regions, x)
        for y in cube.y_coords():
            regions = Space.split_at_y(regions, y)
        for z in cube.z_coords():
            regions = Space.split_at_z(regions, z)
        return set.union(regions, regions_to_keep)

    @staticmethod
    def split_at_x(regions: set[Cube], x):
        new_regions = set()
        while regions:
            region = regions.pop()
            splits = region.split_x(x)
            if not isinstance(splits, set):
                print(splits)
            new_regions.update(splits)
        return new_regions

    @staticmethod
    def split_at_y(regions: set[Cube], y):
        new_regions = set()
        while regions:
            region = regions.pop()
            splits = region.split_y(y)
            new_regions.update(splits)
        return new_regions

    @staticmethod
    def split_at_z(regions: set[Cube], z):
        new_regions = set()
        while regions:
            region = regions.pop()
            splits = region.split_z(z)
            new_regions.update(splits)
        return new_regions

    def count_within(self, cube: Cube):
        self.regions = Space.split_by_cube(self.regions, cube)
        num = 0
        for region in self.regions:
            if region.contained_in_cube(cube):
                num += region.count()
        return num


def part_1(inp):
    operations = []
    for result in inp:
        nums = list(result)
        state = result["state"] == "on"
        operations.append(Operation(cube=Cube(*nums), state=state))
    print(operations)
    space = Space(regions=set())
    for operation in operations:
        space.apply_operation(operation)
    return space.count_within(Cube(-50, 50, -50, 50, -50, 50))


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
    self.assertSetEqual(
        {
            Cube(xmin=11, xmax=11, ymin=9, ymax=10, zmin=11, zmax=11),
            Cube(xmin=11, xmax=11, ymin=11, ymax=11, zmin=10, zmax=10),
            Cube(xmin=9, xmax=10, ymin=11, ymax=11, zmin=10, zmax=10),
            Cube(xmin=11, xmax=11, ymin=9, ymax=10, zmin=10, zmax=10),
            Cube(xmin=9, xmax=10, ymin=9, ymax=10, zmin=10, zmax=10),
            Cube(xmin=9, xmax=10, ymin=11, ymax=11, zmin=9, zmax=9),
            Cube(xmin=9, xmax=10, ymin=9, ymax=10, zmin=9, zmax=9),
            Cube(xmin=9, xmax=10, ymin=11, ymax=11, zmin=11, zmax=11),
            Cube(xmin=9, xmax=10, ymin=9, ymax=10, zmin=11, zmax=11),
            Cube(xmin=11, xmax=11, ymin=11, ymax=11, zmin=9, zmax=9),
            Cube(xmin=11, xmax=11, ymin=9, ymax=10, zmin=9, zmax=9),
            Cube(xmin=11, xmax=11, ymin=11, ymax=11, zmin=11, zmax=11),
        },
        Space.split_by_cube(
            {Cube(xmin=9, xmax=11, ymin=9, ymax=11, zmin=9, zmax=11)},
            Cube(11, 11, 11, 11, 10, 10),
        ),
    )
    inp = read_input("sample_2")
    self.assertEqual(39, part_1(inp))
    inp = read_input("sample_1")
    self.assertEqual(590784, part_1(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
