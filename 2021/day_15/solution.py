from unittest import TestCase

import networkx as nx
from networkx import shortest_path_length


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[int(val) for val in line] for line in lines]  # parse here...
    return inp


def part_1(inp):
    return find_shortest_path_length(inp)


def find_shortest_path_length(inp):
    num_rows = len(inp)
    num_cols = len(inp[0])
    G = get_graph(inp)
    return shortest_path_length(
        G, source=(0, 0), target=(num_rows - 1, num_cols - 1), weight="weight"
    )


def get_graph(inp):
    G = nx.DiGraph()
    for x, row in enumerate(inp):
        for y, val in enumerate(row):
            node = (x, y)
            G.add_node(node, risk=val)
            connect(G, node)
    return G


def connect(G, node):
    x, y = node
    neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for neighbour in neighbours:
        if neighbour not in G:
            continue
        G.add_edge(neighbour, node, weight=G.nodes[node]["risk"])
        G.add_edge(node, neighbour, weight=G.nodes[neighbour]["risk"])


def part_2(inp):
    new_inp = get_new_inp(inp)
    return find_shortest_path_length(new_inp)


def get_new_inp(inp):
    num_rows = len(inp)
    num_cols = len(inp[0])
    new_inp = []
    for j in range(5):
        for y in range(num_rows):
            new_row = []
            for i in range(5):
                for x in range(num_cols):
                    value = (inp[y][x] + i + j - 1) % 9 + 1
                    new_row.append(value)
            new_inp.append(new_row)
    return new_inp


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
    self.assertEqual(40, part_1(inp))
    self.assertEqual(315, part_2(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
