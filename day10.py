import re
import networkx as nx
from parse import *
import copy

with open("input10.txt") as f:
    nums =[int(line.strip()) for line in f.readlines() if line.strip()]

# part 1

sn=[0] + list(sorted(nums))
sn.append(sn[-1]+3)

diffs = [v-u for u,v in zip(sn, sn[1:])]
threes = diffs.count(3)
ones = diffs.count(1)
print(ones, threes, ones*threes)

# part 2
G=nx.DiGraph()

for n in sn:
    G.add_node(n)
    for en in G.nodes:
        if 0< n-en <=3:
            G.add_edge(en, n)

# iterating over all paths is too slow (and we only need the amount of paths, not each of them)
# print(sum(1 for _ in nx.all_simple_paths(G, 0, n)))
num_vals = len(sn)
n_low = sn[0]
m = 1
for n in range(1, num_vals):
    node = sn[n]
    if diffs[n-1] == 3:
        # we can break the chain here and calculate simple paths for each bit separately
        num_paths = sum(1 for _ in nx.all_simple_paths(G, n_low, node))
        m *= num_paths
        n_low = node

print(m)
