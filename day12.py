import re
import networkx as nx
from parse import *
import copy
from collections import defaultdict
import itertools
import numpy as np
from math import cos, sin, pi

with open("input12.txt") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

ins = [
    parse("{}{:d}", line).fixed for line in lines
]

xy = np.array((0., 0.))
d = np.array((1., 0.))


def get_rot_matrix(n):
    return np.array([
        [cos(np.deg2rad(n)), -sin(np.deg2rad(n))],
        [sin(np.deg2rad(n)), cos(np.deg2rad(n))]
    ])


for (i, n) in ins:
    if i == "F":
        xy += d * n
    if i == "N":
        xy += np.array((0, 1)) * n
    if i == "S":
        xy += np.array((0, -1)) * n
    if i == "E":
        xy += np.array((1, 0)) * n
    if i == "W":
        xy += np.array((-1, 0)) * n
    if i == "L":
        m = get_rot_matrix(n)
        d = m.dot(d)
    if i == "R":
        m = get_rot_matrix(-n)
        d = m.dot(d)

print(abs(xy[0]) + abs(xy[1]))

xy = np.array((10., 1.))
xys = np.array((0., 0.))

for (i, n) in ins:
    if i == "F":
        xys += xy * n
    if i == "N":
        xy += np.array((0, 1)) * n
    if i == "S":
        xy += np.array((0, -1)) * n
    if i == "E":
        xy += np.array((1, 0)) * n
    if i == "W":
        xy += np.array((-1, 0)) * n
    if i == "L":
        m = get_rot_matrix(n)
        xy = m.dot(xy)
    if i == "R":
        m = get_rot_matrix(-n)
        xy = m.dot(xy)

print(abs(xys[0]) + abs(xys[1]))
