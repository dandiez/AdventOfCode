import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict
import itertools
import numpy as np


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.x_max = len(lines)
        self.y_max = len(lines[0])
        self.pad = "."
        self.visible = None

    def get(self, x, y):
        if x < 0 or y < 0:
            return self.pad
        try:
            return self.lines[x][y]
        except Exception:
            return self.pad

    def set(self, x, y, value):
        line = list(self.lines[x])
        line[y] = value
        self.lines[x] = "".join(line)

    def subgrid(self, x, y, dx, dy):
        lines = []
        for xx in range(x - dx, x + dx + 1):
            line = ""
            for yy in range(y - dy, y + dy + 1):
                line += self.get(xx, yy)
            lines.append(line)
        return Grid(lines)

    def show(self):
        for line in self.lines:
            print(line)

    def count_char(self, c):
        total = 0
        for line in self.lines:
            total += line.count(c)
        return total

    def get_copy(self):
        lines = copy.deepcopy(self.lines)
        new_g = Grid(lines)
        new_g.visible = self.visible  # reuse same cached list
        return new_g

    def _find_next_visible_seat_in_direction(self, x, y, dx, dy, max_distance=np.inf):
        if dx == 0 and dy == 0:
            return None
        xx = x
        yy = y
        d = 0
        while (0 <= xx <= g.x_max) and (0 <= yy <= g.y_max) and (d < max_distance):
            xx += dx
            yy += dy
            d += 1
            if g.get(xx, yy) in ["L", "#"]:
                return (xx, yy)
        return None

    def _find_all_visible_seats(self, x, y, max_distance=np.inf):
        visible = []
        for (dx, dy) in itertools.product((-1, 0, 1), repeat=2):
            seat = g._find_next_visible_seat_in_direction(
                x, y, dx, dy, max_distance=max_distance
            )
            if seat is not None:
                visible.append(seat)
        return visible

    def cache_visible_seats(self, max_distance=np.inf):
        """Keep a dict which has all visible seats at every location of the grid {(x,y):[(x0, y0), (x1, y1),...]}"""
        if self.visible is not None:
            # do not recalculate cache if already done
            return
        visible_seats = dict()
        for (x, y) in self.iterate_grid():
            visible_seats[(x, y)] = g._find_all_visible_seats(
                x, y, max_distance=max_distance
            )
        self.visible = visible_seats

    def iterate_grid(self):
        for (n, m) in itertools.product(range(self.x_max), range(self.y_max)):
            yield (n, m)


def iterate_solve_grid(orig_grid, max_distance, occupancy_limit):
    orig_grid.cache_visible_seats(max_distance=max_distance)
    grid = orig_grid.get_copy()
    changed = False
    for (n, m) in grid.iterate_grid():
        neighbour_seats = [orig_grid.get(xx, yy) for (xx, yy) in grid.visible[(n, m)]]
        num_occupied = neighbour_seats.count("#")
        if orig_grid.get(n, m) == "L" and num_occupied == 0:
            grid.set(n, m, "#")
            changed = True
        if orig_grid.get(n, m) == "#" and num_occupied >= occupancy_limit:
            grid.set(n, m, "L")
            changed = True
    print(".", end="")
    return changed, grid


def full_solve_grid(g, *args):
    last_changed = True
    while last_changed:
        last_changed, g = iterate_solve_grid(g, *args)
    return g


def part_2(g):
    solved_g = full_solve_grid(g, np.inf, 5)
    print("\npart 2:", solved_g.count_char("#"))


def part_1(g):
    solved_g = full_solve_grid(g, 1, 4)
    print("\npart 1:", solved_g.count_char("#"))


with open("input11.txt") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

g = Grid(lines)
# g.show()
part_1(g.get_copy())
part_2(g)
