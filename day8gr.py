import re
import networkx as nx
from parse import *
import copy

with open("input8.txt") as f:
    lines =[line.strip() for line in f.readlines() if line.strip()]

operations = {n:parse("{} {:d}", lines[n]).fixed for n in range(len(lines))}

G = nx.DiGraph()

for k, v in operations.items():
    ins, num = v
    G.add_node(k, ins=ins, num=num)
    if ins=="jmp":
        G.add_edge(k, k+num)
    else:
        G.add_edge(k, k+1)


# part 1
def run(G, start=0):
    s=0
    for n in nx.dfs_successors(G, start):
        if G.nodes[n]["ins"]=="acc":
            s+= G.nodes[n]["num"] 
    is_inf_loop = list(G.successors(n))[0] < max(G.nodes)
    return s, is_inf_loop

print(run(G))

# part 2
def mod_G(G):
    orig_G = G.copy()
    for n in G.nodes:
        G = orig_G.copy()
        ins, num =G.nodes[n]["ins"], G.nodes[n]["num"]
        if ins=="nop":
            G.add_node(n, ins="jmp", num=num)
            G.add_edge(n, n + num)
        elif ins=="jmp":
            G.add_node(n, ins="nop", num=num)
            G.remove_edge(n, n + num)
            G.add_edge(n, n + 1)
        yield G


for g in mod_G(G):
    s, is_inf = run(g)
    if not is_inf:
        print(s)
        break

