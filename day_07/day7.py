import re
import networkx as nx

with open("input7.txt") as f:
    lines =[line.strip() for line in f.readlines() if line.strip()]

G = nx.DiGraph()

for line in lines:
    N, rest = line.split(" bags contain ")
    if rest == "no other bags.":
        G.add_node(N)
        continue
    rels = [ b.strip() for b in re.split("[,.]", rest) if b.strip()]
    for rel in rels:
        num, col1, col2, _ = rel.split(" ")
        color = col1 + " " + col2
        G.add_node(color)
        G.add_edge(N, color, amount=int(num))

print(len(nx.ancestors(G, "shiny gold")))

# part 2
def bags_inside(source):
    tot = 0
    for n in G.successors(source):
        tot += G.get_edge_data(source, n)["amount"] * ( 1 + bags_inside(n) )
    return tot

print(bags_inside("shiny gold"))
