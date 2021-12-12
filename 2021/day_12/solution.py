import copy
from collections import defaultdict
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [tuple(line.split("-")) for line in lines]  # parse here...
    return inp


def part_1(inp):

    pass


def part_2(inp):
    caves = Caves(inp)
    return sum(1 for path in caves.yield_paths("start", "end", single_small_visited=False))


class Caves:
    def __init__(self, inp: list[tuple[str, str]]):
        self.nodes: dict[str, list[str]] = defaultdict(list)
        self._populate_nodes(inp)

    def _populate_nodes(self, inp):
        for a, b in inp:
            self.nodes[a].append(b)
            self.nodes[b].append(a)

    def yield_paths(self, from_node, to_node, visited_small=None, path_so_far=None, single_small_visited=None):
        # print(from_node, to_node, visited_small, path_so_far, single_small_visited)
        if from_node=='end':
            return
        visited_small = visited_small or {from_node}
        path_so_far = path_so_far or [from_node]
        for neighbour_node in self.nodes[from_node]:
            if neighbour_node == to_node:
                yield path_so_far
            if neighbour_node == 'start':
                    continue
            new_single_small_visited = single_small_visited
            if neighbour_node in visited_small:
                if single_small_visited == True:
                    continue
                else:
                    new_single_small_visited = True
            new_visited_small = copy.deepcopy(visited_small)
            new_path_so_far = copy.deepcopy(path_so_far)
            if neighbour_node.lower() == neighbour_node:
                new_visited_small.add(neighbour_node)
            new_path_so_far.append(neighbour_node)
            yield from self.yield_paths(
                neighbour_node,
                to_node,
                visited_small=new_visited_small,
                path_so_far=new_path_so_far,
                single_small_visited=new_single_small_visited
            )


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
    self.assertEqual(36, part_2(inp))
    inp = read_input("sample_2")
    self.assertEqual(103, part_2(inp))
    inp = read_input("sample_3")
    self.assertEqual(3509, part_2(inp))

def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
