import copy
from collections import defaultdict
from unittest import TestCase

DEBUG_PRINT_PATHS = False


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [tuple(line.split("-")) for line in lines]  # parse here...
    return inp


def part_1(inp):
    caves = Caves(inp)
    return sum(
        1
        for path in caves.yield_paths(
            "start", "end", False, double_visit_was_used=False
        )
    )


def part_2(inp):
    caves = Caves(inp)
    return sum(
        1
        for path in caves.yield_paths("start", "end", True, double_visit_was_used=False)
    )


class Caves:
    def __init__(self, inp: list[tuple[str, str]]):
        self.nodes: dict[str, list[str]] = defaultdict(list)
        self._populate_nodes(inp)

    def _populate_nodes(self, inp):
        for a, b in inp:
            self.nodes[a].append(b)
            self.nodes[b].append(a)

    def yield_paths(
        self,
        from_cave,
        to_cave,
        allow_double_small_visit,
        visited_small_caves=None,
        path_so_far=None,
        double_visit_was_used=False,
    ):
        if from_cave == "end":
            if DEBUG_PRINT_PATHS:
                print(f"Unique path found: {','.join(path_so_far)}")
            return
        visited_small_caves = visited_small_caves or {from_cave}
        path_so_far = path_so_far or [from_cave]
        for neighbour_cave in self.nodes[from_cave]:
            if neighbour_cave == to_cave:
                yield path_so_far
            if neighbour_cave == "start":
                continue
            new_double_visit_was_used = double_visit_was_used
            if neighbour_cave in visited_small_caves:
                if double_visit_was_used or not allow_double_small_visit:
                    continue
                else:
                    new_double_visit_was_used = True
            new_visited_small_caves = copy.deepcopy(visited_small_caves)
            new_path_so_far = copy.deepcopy(path_so_far)
            if neighbour_cave.lower() == neighbour_cave:
                new_visited_small_caves.add(neighbour_cave)
            new_path_so_far.append(neighbour_cave)
            yield from self.yield_paths(
                neighbour_cave,
                to_cave,
                allow_double_small_visit,
                visited_small_caves=new_visited_small_caves,
                path_so_far=new_path_so_far,
                double_visit_was_used=new_double_visit_was_used,
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
