from collections import defaultdict
from itertools import combinations
from unittest import TestCase

import networkx as nx
import numpy as np
from numpy.linalg import linalg
from scipy.spatial.distance import cityblock
from scipy.spatial.transform import Rotation


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


def get_all_rotations():
    yield from [Rotation.from_euler("x", 90 * i, degrees=True) for i in range(4)]
    yield from [Rotation.from_euler("zx", [90, 90 * i], degrees=True) for i in range(4)]
    yield from [
        Rotation.from_euler("zx", [180, 90 * i], degrees=True) for i in range(4)
    ]
    yield from [
        Rotation.from_euler("zx", [-90, 90 * i], degrees=True) for i in range(4)
    ]
    yield from [Rotation.from_euler("yx", [90, 90 * i], degrees=True) for i in range(4)]
    yield from [
        Rotation.from_euler("yx", [-90, 90 * i], degrees=True) for i in range(4)
    ]


def part_1(inp):
    overlap_transformations = trans_overlapping(inp)
    transformations = trans_rel_to_0(overlap_transformations)
    abs_point_coords = all_points_rel_to_0(inp, transformations)
    max_d = find_largest_manhattan(transformations)
    print(max_d)
    return len(abs_point_coords)


def find_largest_manhattan(transformations):
    max_d = 0
    for i, vi in transformations.items():
        for j, vj in transformations.items():
            if i == j:
                continue
            pi = vi[:, -1]
            pj = vj[:, -1]
            d = cityblock(pi, pj)
            max_d = max(max_d, d)
    return max_d


def trans_overlapping(inp):
    """Find the transformations across scanners overlapping.

    Return dict of transformation matrices across overlapping scanners.
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


def trans_rel_to_0(overlaps):
    """Chain transformations to arrive at any target from zero."""
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


def find_best_shift(points_1, points_2):
    """Given two clouds of points, find the shift that overlaps most points.
    The shift is given as column vector.
    """
    p1s = [as_int(a) for a in points_1]
    p2s = [as_int(a) for a in points_2]
    differences = defaultdict(int)
    for p1 in p1s:
        for p2 in p2s:
            differences[tuple(p1 - p2)] += 1
    most_in_common = max(differences.values())
    for k, v in differences.items():
        if v == most_in_common:
            return np.array([k], int).T, v


def as_int(arr):
    return np.rint(arr).astype(int)


def all_points_rel_to_0(inp, transformations):
    """Use the transformations to express all points in abs. coordinates."""
    abs_points = set()
    for csys, points in inp.items():
        trn = transformations[csys]
        point_cloud = np.vstack((np.array(points).T, np.ones(len(points))))
        abs_csys_points = np.matmul(trn, point_cloud)
        abs_csys_points = abs_csys_points[:-1].T.tolist()
        abs_csys_points = set(tuple(p) for p in abs_csys_points)
        abs_points.update(abs_csys_points)
    return abs_points



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
    self.assertEqual(79, part_1(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
