import re
import networkx as nx
from parse import *
import copy

with open("input9.txt") as f:
    nums = [int(line.strip()) for line in f.readlines() if line.strip()]

# part 1
preamble = 25
for n in range(preamble, len(nums)):
    num = nums[n]
    found_pair = False
    for u in range(n - preamble, n):
        for v in range(n - preamble, n):
            if nums[u] == nums[v]:
                continue
            if nums[u] + nums[v] == num:
                found_pair = True
                break
    if not found_pair:
        print(n, num)
        break

# part 2
target = num
for n in range(0, len(nums)):
    s = nums[n]
    for v in range(n + 1, len(nums)):
        s += nums[v]
        if s == target:
            print(
                min([nums[k] for k in range(n, v + 1)])
                + max([nums[k] for k in range(n, v + 1)])
            )
            1 / 0
        elif s > target:
            continue
