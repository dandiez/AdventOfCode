import dataclasses
from collections import defaultdict
from functools import lru_cache
from unittest import TestCase

DEBUG_PRINT_PATHS = False


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [tuple(line.split("-")) for line in lines]  # parse here...
    return inp


def part_1(inp):
    caves = Caves(inp)
    return count_paths_to_target_cave(
        caves=caves.nodes,
        visit_state=VisitState(current_cave="start"),
        target_cave="end",
        allow_double_small_visit=False,
    )


def part_2(inp):
    caves = Caves(inp)
    return count_paths_to_target_cave(
        caves=caves.nodes,
        visit_state=VisitState(current_cave="start"),
        target_cave="end",
        allow_double_small_visit=True,
    )


def count_paths_to_target_cave(
    *, caves, visit_state: "VisitState", target_cave, allow_double_small_visit
):
    paths_to_target = 0
    for neighbour_cave in caves[visit_state.current_cave]:
        if neighbour_cave == target_cave:
            paths_to_target += 1
        elif visit_state.cave_visit_allowed(neighbour_cave, allow_double_small_visit):
            neighbour_cave_state = visit_state.get_visit_neighbour_cave_state(
                neighbour_cave
            )
            paths_to_target += count_paths_to_target_cave(
                caves=caves,
                visit_state=neighbour_cave_state,
                target_cave=target_cave,
                allow_double_small_visit=allow_double_small_visit,
            )
    return paths_to_target


@dataclasses.dataclass
class VisitState:
    current_cave: str
    visited_small_caves: set[str] = dataclasses.field(default_factory=set)
    double_visit_was_used: bool = False
    # path_to_current_cave: list[str] = dataclasses.field(default_factory=list)

    def get_visit_neighbour_cave_state(self, neighbour_to_visit):
        # Assumes the cave to visit is a valid cave
        neighbour_state = VisitState(
            current_cave=neighbour_to_visit,
            visited_small_caves=self.visited_small_caves.copy(),
            double_visit_was_used=self.double_visit_was_used,
            # path_to_current_cave=self.path_to_current_cave.copy(),
        )
        # neighbour_state.path_to_current_cave.append(neighbour_state.current_cave)
        if (
            neighbour_state.current_cave in neighbour_state.visited_small_caves
            and cave_is_small(neighbour_state.current_cave)
        ):
            neighbour_state.double_visit_was_used = True
        else:
            neighbour_state.visited_small_caves.add(neighbour_state.current_cave)
        return neighbour_state

    def cave_visit_allowed(self, cave, allow_double_small_visits):
        if cave == "start":
            return False
        if not cave_is_small(cave):
            return True
        if not allow_double_small_visits:
            # part 1
            return cave not in self.visited_small_caves
        # part 2
        if self.double_visit_was_used and cave in self.visited_small_caves:
            return False
        return True


@lru_cache(None)
def cave_is_small(cave):
    return cave.islower()


class Caves:
    def __init__(self, inp: list[tuple[str, str]]):
        self.nodes: dict[str, list[str]] = defaultdict(list)
        self._populate_nodes(inp)

    def _populate_nodes(self, inp):
        for a, b in inp:
            self.nodes[a].append(b)
            self.nodes[b].append(a)


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
    self.assertEqual(10, part_1(inp))
    inp = read_input("sample_2")
    self.assertEqual(19, part_1(inp))
    inp = read_input("sample_3")
    self.assertEqual(226, part_1(inp))

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
