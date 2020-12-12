import re
import networkx as nx
from parse import *
import copy

with open("input10.txt") as f:
    nums =[int(line.strip()) for line in f.readlines() if line.strip()]

# part 1
nums.sort()
sn=[0] + nums + [nums[-1] +3]

diffs = [v-u for u,v in zip(sn, sn[1:])]
threes = diffs.count(3)
ones = diffs.count(1)
print(ones, threes, ones*threes)

# part 2

# ways = {step_height: number_of_ways_to_get_there}
step_heights = sn
ways = dict()
ways[step_heights[0]] = 1

def can_reach(from_step_height, to_step_height):
    if (to_step_height-3) <= from_step_height < to_step_height:
        return True
    return False

def ways_to_get_to_step_of_height(height):
    if height in ways.keys():
        return ways[height]
    w = sum( [ ways_to_get_to_step_of_height(lower_step_height) for lower_step_height in step_heights if can_reach(lower_step_height, height)])
    ways[height] = w
    return w

heighest_step = step_heights[-1]
print(ways_to_get_to_step_of_height(heighest_step))
