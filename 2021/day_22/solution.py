import dataclasses
from functools import lru_cache
from unittest import TestCase

from parse import parse


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [
        parse("{state} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line) for line in lines
    ]
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

    def all_points(self):
        for x in range(self.xmin, self.xmax):
            for y in range(self.ymin, self.ymax):
                for z in range(self.zmin, self.zmax):
                    yield x, y, z

    @lru_cache()
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

    def merge(self, other):
        within_dx = self.xmin == other.xmin and self.xmax == other.xmax
        within_dy = self.ymin == other.ymin and self.ymax == other.ymax
        within_dz = self.zmin == other.zmin and self.zmax == other.zmax
        if within_dz and within_dy:
            if self.xmax + 1 == other.xmin:
                return Cube(
                    self.xmin, other.xmax, self.ymin, other.ymax, self.zmin, other.zmax
                )
            elif other.xmax + 1 == self.xmin:
                return Cube(
                    other.xmin, self.xmax, other.ymin, self.ymax, other.zmin, self.zmax
                )
        elif within_dx and within_dy:
            if self.zmax + 1 == other.zmin:
                return Cube(
                    self.xmin, other.xmax, self.ymin, other.ymax, self.zmin, other.zmax
                )
            elif other.zmax + 1 == self.zmin:
                return Cube(
                    other.xmin, self.xmax, other.ymin, self.ymax, other.zmin, self.zmax
                )
        elif within_dz and within_dx:
            if self.ymax + 1 == other.ymin:
                return Cube(
                    self.xmin, other.xmax, self.ymin, other.ymax, self.zmin, other.zmax
                )
            elif other.ymax + 1 == self.ymin:
                return Cube(
                    other.xmin, self.xmax, other.ymin, self.ymax, other.zmin, self.zmax
                )
        return None

    def difference(self, other):
        """Given another cube, split this one and only keep the parts not in common with the other."""
        split_self = Space.split_by_cube({self}, other)
        remaining = {
            split for split in split_self if not split.contained_in_cube(other)
        }
        return Space.simplify(remaining)


@dataclasses.dataclass
class Operation:
    cube: Cube
    state: bool


@dataclasses.dataclass
class Space:
    regions: set[Cube]

    @staticmethod
    def count(regions):
        return sum(r.count() for r in regions)

    def apply_operation(self, operation: Operation, scope: Cube):
        cube = operation.cube
        if not cube.contained_in_cube(scope):
            return
        if operation.state is True:
            subcubes = Space.split_by_many_cubes({cube}, self.regions)
            skip = set()
            for cube in subcubes:
                for region in self.regions:
                    if cube.contained_in_cube(region):
                        skip.add(cube)
            not_skipped = subcubes.difference(skip)
            self.regions.update(not_skipped)
        else:
            self.regions = self.subtract_cube_from_regions(self.regions, cube)
        self.regions = Space.stubborn_simplify(self.regions)

    @staticmethod
    def subtract_cube_from_regions(regions, cube):
        new_regions = set()
        while regions:
            region: Cube = regions.pop()
            new_regions.update(region.difference(cube))
        return new_regions

    def assert_valid_region(self):
        for r in self.regions:
            for rr in self.regions:
                if r != rr:
                    assert r.do_not_overlap_for_sure(rr), f"{r}, {rr}"

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

    @staticmethod
    def simplify(regions):
        non_simplifiable = set()
        while regions:
            reg = regions.pop()
            merged, merge_happened = Space.merge(regions, reg)
            if not merge_happened:
                non_simplifiable.add(reg)
                regions = merged
            else:
                regions = merged
        return non_simplifiable

    @staticmethod
    def stubborn_simplify(regions):
        num = len(regions)
        while True:
            regions = Space.simplify(regions)
            if num == len(regions):
                break
            else:
                num = len(regions)
        return regions

    @staticmethod
    def merge(regions: set[Cube], to_merge: Cube):
        merged_set = set()
        merge_happened = False
        while regions:
            other = regions.pop()
            merged = to_merge.merge(other)
            if merged is not None:
                merged_set.add(merged)
                merge_happened = True
                merged_set.update(regions)
                break
            else:
                merged_set.add(other)
        return merged_set, merge_happened


def part_1(inp, scope=Cube(-50, 50, -50, 50, -50, 50)):
    operations = []
    for result in inp:
        nums = list(result)
        state = result["state"] == "on"
        operations.append(Operation(cube=Cube(*nums), state=state))
    print(operations)
    space = Space(regions=set())
    num_operations = len(operations)
    for n, operation in enumerate(operations):
        print(f"{n} / {num_operations}")
        space.apply_operation(operation, scope)
    return space.count_within(scope)


def part_2(inp):
    return part_1(
        inp,
        Cube(-50000000, 500000000, -5000000000, 5000000000, -5000000000, 5000000000),
    )


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
    inp = read_input("sample_2")
    self.assertEqual(39, part_1(inp))
    inp = read_input("sample_1")
    self.assertEqual(590784, part_1(inp))
    inp = read_input("sample_3")
    self.assertEqual(2758514936282235, part_2(inp))


def test_methods(self):
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
    self.assertEqual(
        {Cube(9, 11, 11, 11, 9, 10)},
        Space.simplify(
            {
                Cube(xmin=9, xmax=11, ymin=11, ymax=11, zmin=10, zmax=10),
                Cube(xmin=9, xmax=11, ymin=11, ymax=11, zmin=9, zmax=9),
            }
        ),
    )
    self.assertEqual(
        {Cube(9, 11, 9, 11, 9, 11)},
        Space.stubborn_simplify(
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
            }
        ),
    )
    self.assertEqual(
        Cube(1, 2, 3, 3, 3, 3), Cube(1, 1, 3, 3, 3, 3).merge(Cube(2, 2, 3, 3, 3, 3))
    )
    self.assertEqual(
        {Cube(1, 2, 1, 2, 1, 2)},
        Space.stubborn_simplify(
            {
                Cube(i, i, j, j, k, k)
                for i in range(1, 3)
                for j in range(1, 3)
                for k in range(1, 3)
            }
        ),
    )
    self.assertEqual(
        Cube(xmin=9, xmax=11, ymin=9, ymax=11, zmin=9, zmax=11).count(),
        sum(
            cube.count()
            for cube in Space.stubborn_simplify(
                {
                    Cube(xmin=10, xmax=10, ymin=11, ymax=11, zmin=10, zmax=10),
                    Cube(xmin=11, xmax=11, ymin=9, ymax=9, zmin=10, zmax=10),
                    Cube(xmin=9, xmax=9, ymin=9, ymax=10, zmin=10, zmax=10),
                    Cube(xmin=9, xmax=9, ymin=11, ymax=11, zmin=9, zmax=9),
                    Cube(xmin=11, xmax=11, ymin=10, ymax=10, zmin=11, zmax=11),
                    Cube(xmin=10, xmax=10, ymin=10, ymax=10, zmin=10, zmax=10),
                    Cube(xmin=11, xmax=11, ymin=9, ymax=9, zmin=11, zmax=11),
                    Cube(xmin=9, xmax=9, ymin=11, ymax=11, zmin=11, zmax=11),
                    Cube(xmin=10, xmax=10, ymin=9, ymax=10, zmin=9, zmax=9),
                    Cube(xmin=11, xmax=11, ymin=9, ymax=10, zmin=9, zmax=9),
                    Cube(xmin=10, xmax=10, ymin=11, ymax=11, zmin=9, zmax=9),
                    Cube(xmin=10, xmax=10, ymin=11, ymax=11, zmin=11, zmax=11),
                    Cube(xmin=11, xmax=11, ymin=11, ymax=11, zmin=10, zmax=10),
                    Cube(xmin=10, xmax=10, ymin=9, ymax=9, zmin=10, zmax=10),
                    Cube(xmin=11, xmax=11, ymin=10, ymax=10, zmin=10, zmax=10),
                    Cube(xmin=9, xmax=9, ymin=11, ymax=11, zmin=10, zmax=10),
                    Cube(xmin=9, xmax=9, ymin=9, ymax=10, zmin=9, zmax=9),
                    Cube(xmin=11, xmax=11, ymin=11, ymax=11, zmin=9, zmax=9),
                    Cube(xmin=9, xmax=9, ymin=9, ymax=10, zmin=11, zmax=11),
                    Cube(xmin=10, xmax=10, ymin=9, ymax=9, zmin=11, zmax=11),
                    Cube(xmin=10, xmax=10, ymin=10, ymax=10, zmin=11, zmax=11),
                    Cube(xmin=11, xmax=11, ymin=11, ymax=11, zmin=11, zmax=11),
                }
            )
        ),
    )

    a = Cube(xmin=-46, xmax=-23, ymin=-6, ymax=46, zmin=-46, zmax=-1)
    b = Cube(xmin=-48, xmax=-32, ymin=26, ymax=41, zmin=-47, zmax=-37)
    self.assertTrue(b.contains((-46, 30, -38)))
    all_points_in_a = set(a.all_points())
    all_points_in_b = set(b.all_points())
    delta = all_points_in_a.difference(all_points_in_b)
    d = Space.subtract_cube_from_regions({a}, b)
    # self.assertEqual(len(delta), Space.count(a.difference(b)))
    # self.assertEqual(len(delta), Space.count(d))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_methods(TestCase())
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
