import dataclasses
import re
from typing import Iterable
from unittest import TestCase

CutPoint = tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Segment:
    xmin: int
    xmax: int

    @property
    def length(self):
        return self.xmax - self.xmin + 1

    def get_cut_points_from_end_points(self) -> Iterable[CutPoint]:
        yield (self.xmin - 1, self.xmin)
        yield (self.xmax, self.xmax + 1)

    def __contains__(self, x: int):
        return self.xmin <= x <= self.xmax

    def split(self, p: CutPoint) -> Iterable['Segment']:
        if p[0] not in self or p[1] not in self:
            yield self
            return
        yield Segment(self.xmin, p[0])
        yield Segment(p[1], self.xmax)


@dataclasses.dataclass
class Row:
    y: int
    segments: set[Segment]

    def __contains__(self, item: Segment):
        return item in self.segments

    def split(self, p: CutPoint):
        new_set = set()
        for segment in self.segments:
            for split in segment.split(p):
                new_set.add(split)
        self.segments = new_set

    def subtract(self, s: Segment):
        self.segments.difference_update({s})

    def simplify(self):
        cut_points = self.get_all_end_point_cut_points()
        for cp in cut_points:
            self.split(cp)

    def get_all_end_point_cut_points(self):
        return {cp for s in self.segments for cp in s.get_cut_points_from_end_points()}

    def cell_sum(self):
        self.simplify()
        return sum(s.length for s in self.segments)

    def contiguous(self):
        l = list([(s.xmin, s.xmax) for s in self.segments])
        l.sort()
        for s1, s2 in zip(l, l[1:]):
            if s1[1] != s2[0]:
                return False
        return True


@dataclasses.dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int
    radius: int = None

    def __post_init__(self):
        self.radius = abs(self.beacon_x - self.x) + abs(self.beacon_y - self.y)

    @classmethod
    def from_string(cls, s):
        numbs = [int(s) for s in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", s)]
        return cls(*numbs)

    def intersect_at_y(self, y, subtract_beacon=False) -> Row:
        if abs(y - self.y) > self.radius:
            return Row(y=y, segments=set())
        minx = self.x - (self.radius - abs(y - self.y))
        maxx = self.x + (self.radius - abs(y - self.y))
        segment = Segment(minx, maxx)
        r = Row(y=y, segments={segment})
        if self.beacon_y == y and subtract_beacon:
            r.split((self.beacon_x - 1, self.beacon_x))
            r.split((self.beacon_x, self.beacon_x + 1))
            r.subtract(Segment(self.beacon_x, self.beacon_x))
        return r


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [Sensor.from_string(s) for s in lines]  # parse here...
    return inp


def part_1(inp, y=2000000):
    not_there = Row(y=y, segments=set())
    for sensor in inp:
        for intersect_segment in sensor.intersect_at_y(y, subtract_beacon=True).segments:
            not_there.segments.add(intersect_segment)
    return not_there.cell_sum()


def part_2(inp, largest_coord=4000000):
    limits = {(-1, 0), (largest_coord, largest_coord + 1)}
    for y in range(largest_coord):
        if y % 100000 == 0:
            print(y)
        not_there = Row(y=y, segments=set())
        for sensor in inp:
            for intersect_segment in sensor.intersect_at_y(y).segments:
                not_there.segments.add(intersect_segment)
        for l in limits:
            not_there.split(l)
        exclude = set()
        for s in not_there.segments:
            if s.xmin < 0:
                exclude.add(s)
            if s.xmax > largest_coord:
                exclude.add(s)
        for s in exclude:
            not_there.subtract(s)
        if not_there.contiguous():
            continue
        whole_row = Row(segments={Segment(0, largest_coord)}, y=y)
        all_cp = not_there.get_all_end_point_cut_points()
        for cp in all_cp:
            not_there.split(cp)
            whole_row.split(cp)
        for s in not_there.segments:
            whole_row.subtract(s)
        if whole_row.segments:
            s = whole_row.segments.pop()
            return s.xmin * 4000000 + whole_row.y


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
    self.assertEqual(26, part_1(inp, 10))


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(56000011, part_2(inp, largest_coord=20))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
