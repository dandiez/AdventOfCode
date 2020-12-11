import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict

with open("input11.txt") as f:
    lines =[line.strip() for line in f.readlines() if line.strip()]

# part 1

class Grid():
    def __init__(self, lines):
        self.lines = lines
        self.x_max = len(lines)
        self.y_max = len(lines[0])
        self.pad = "."

    def get(self, x, y):
        if x < 0 or y < 0:
            return self.pad
        try:
            return self.lines[x][y]
        except Exception:
            return self.pad

    def set(self, x, y, value):
        line = list( self.lines[x] )
        line[y] = value
        self.lines[x] = "".join( line)

    def subgrid(self, x, y, dx, dy):
        lines = []
        for xx in range(x-dx, x+dx+1):
            line = ""
            for yy in range(y-dy, y+dy+1):
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
        return Grid(lines)


g = Grid(lines)
g.show()



def simulate_grid(orig_grid):
    grid = orig_grid.get_copy()
    changed = False
    for n in range(grid.x_max):
        for m in range(grid.y_max):
            adjacent = orig_grid.subgrid(n, m, 1, 1)
            if orig_grid.get(n,m) == "L":
                if adjacent.count_char("#") == 0:
                    grid.set(n,m, "#")
                    changed = True
            if orig_grid.get(n,m) == "#":
                if adjacent.count_char("#") >=5:
                    grid.set(n,m, "L")
                    changed = True
    print("calculation done")
    #print(grid.show())
    return changed, grid

last_changed = True
while last_changed:
    last_changed, g = simulate_grid(g)


print(g.count_char("#"))