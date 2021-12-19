from collections import defaultdict
from itertools import combinations
from unittest import TestCase

import networkx as nx
import numpy as np
from numpy.linalg import linalg
from scipy.spatial.distance import cityblock
from scipy.spatial.transform import Rotation as R


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    inp = read_input(input_file)
    transformations = get_all_transformations(inp)
    p1 = part_1(inp, transformations)
    print(f"Solution to part 1: {p1}")
    p2 = part_2(transformations)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return parse_inp(lines)


def parse_inp(inp):
    raw = defaultdict(list)
    n = -1
    for line in inp:
        if "scanner" in line:
            n += 1
            continue
        raw[n].append(np.array([int(val) for val in line.split(",")], int))
    return raw


def get_all_transformations(inp):
    """Find transf. matrices for all scanners. Absolute is scanner zero."""
    rel_transf = find_rel_transformations(inp)
    abs_transf = find_abs_transformations(rel_transf)
    return abs_transf


def find_rel_transformations(inp):
    """Return dict of transformation matrices across overlapping scanners.
    { (i, j): np.array() }
    """
    num_scanners = len(inp)
    overlaps = {}
    for i, j in combinations(range(num_scanners), 2):
        transformation = scanners_overlap(inp[i], inp[j])
        if transformation is not None:
            overlaps[(i, j)] = transformation
            overlaps[(j, i)] = as_int(linalg.inv(transformation))
    return overlaps


def scanners_overlap(points_1, points_2):
    """Figure out if scanners have an overlap of common points.

    Return the transformation matrix for the overlap.
    Return None if there is no overlap.
    """
    for r in get_all_rotations():
        points_2_trans = r.apply(points_2)
        best_shift, num_overlaps = find_best_shift(points_1, points_2_trans)
        if num_overlaps >= 12:
            transformation = np.block(
                [[as_int(r.as_matrix()), best_shift], [np.zeros(3, int), np.array([1])]]
            )
            return transformation


def as_int(arr):
    return np.rint(arr).astype(int)


def get_all_rotations():
    yield from [R.from_euler("x", 90 * i, degrees=True) for i in range(4)]
    yield from [R.from_euler("zx", [90, 90 * i], degrees=True) for i in range(4)]
    yield from [R.from_euler("zx", [180, 90 * i], degrees=True) for i in range(4)]
    yield from [R.from_euler("zx", [-90, 90 * i], degrees=True) for i in range(4)]
    yield from [R.from_euler("yx", [90, 90 * i], degrees=True) for i in range(4)]
    yield from [R.from_euler("yx", [-90, 90 * i], degrees=True) for i in range(4)]


def find_best_shift(points_1, points_2):
    """Given two clouds of points, find the shift that overlaps most points.
    The shift is given as column vector.
    Also return the number of points overlapping for that shift.
    """
    p1s = [as_int(a) for a in points_1]
    p2s = [as_int(a) for a in points_2]
    shifts = defaultdict(int)
    for p1 in p1s:
        for p2 in p2s:
            shifts[tuple(p1 - p2)] += 1
    max_points_overlapping = max(shifts.values())
    for shift, num_overlapping in shifts.items():
        if num_overlapping == max_points_overlapping:
            return np.array([shift], int).T, num_overlapping


def find_abs_transformations(overlaps):
    """Chain transformations to arrive at any target from the zero scanner."""
    transformations = {}
    G = nx.Graph()
    G.add_edges_from(overlaps.keys())
    paths = nx.shortest_path(G, source=0)
    for target, path in paths.items():
        trn = np.identity(4, int)
        for n in range(len(path) - 1):
            trn = np.matmul(trn, overlaps[(path[n], path[n + 1])])
        transformations[target] = trn
    return transformations


def part_1(inp, transformations):
    abs_point_coords = all_abs_points(inp, transformations)
    return len(abs_point_coords)


def all_abs_points(inp, transformations):
    """Express all points in absolute coordinates."""
    abs_points = set()
    for csys, points in inp.items():
        trn = transformations[csys]
        point_cloud = np.vstack((np.array(points).T, np.ones(len(points))))
        point_cloud_abs = np.matmul(trn, point_cloud)
        point_cloud_abs = point_cloud_abs[:-1].T.tolist()
        point_cloud_abs = set(tuple(p) for p in point_cloud_abs)
        abs_points.update(point_cloud_abs)
    return abs_points


def part_2(transformations):
    max_d = 0
    for (i, vi), (j, vj) in combinations(transformations.items(), 2):
        pi = vi[:, -1]
        pj = vj[:, -1]
        d = cityblock(pi, pj)
        max_d = max(max_d, d)
    return max_d


def test_sample_1(self):
    self.assertEqual((79, 3621), main("sample_1"))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
