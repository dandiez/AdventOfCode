import dataclasses
import itertools
from unittest import TestCase
import networkx as nx

Location = str

ReleasedFlow = int
TIME_TO_OPEN_ONE_VALVE = 1


@dataclasses.dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    tunnels_to: tuple[str]

    @classmethod
    def from_str(cls, line: str):
        v = line[6:8]
        fr = int(line.split(";")[0].split("=")[1])
        try:
            leads_to = line.split("lead to valves ")[1]
        except Exception:
            leads_to = line.split("leads to valve ")[1]
        tunnels = tuple(v.strip() for v in leads_to.split(","))
        return cls(name=v, flow_rate=fr, tunnels_to=tunnels)


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    vs = [Valve.from_str(line) for line in lines]
    return {v.name: v for v in vs}


@dataclasses.dataclass(frozen=True)
class Progress:
    time_left: int
    released_flow: int
    current_flow_rate: int
    visited: set
    to_visit: set
    current: str

    @property
    def key(self):
        return frozenset(self.visited)

    @property
    def value(self):
        return self.released_flow

    def visit(self, target, time_needed, valves):
        return Progress(
            time_left=self.time_left - time_needed,
            released_flow=time_needed * self.current_flow_rate + self.released_flow,
            current_flow_rate=self.current_flow_rate + valves[target].flow_rate,
            visited=set.union({target}, self.visited),
            to_visit=set.difference(self.to_visit, {target}),
            current=target,
        )

    def wait(self):
        return Progress(
            time_left=0,
            released_flow=self.time_left * self.current_flow_rate + self.released_flow,
            current_flow_rate=self.current_flow_rate,
            visited=self.visited,
            to_visit=self.to_visit,
            current=self.current,
        )


class BestSoFar(dict[frozenset, ReleasedFlow]):
    """Keep track of the best outcomes."""

    def add_from_progress(self, p: Progress):
        if self.is_better_than_existing(p):
            self[p.key] = p.value

    def is_better_than_existing(self, p: Progress):
        if p.key not in self:
            return True
        return p.released_flow > self[p.key]


@dataclasses.dataclass
class Solver:

    valves: dict[Location, Valve]
    time_to_valve: dict[tuple[Location, Location], int] = None
    best_so_far: BestSoFar = None

    def __post_init__(self):

        (
            self.time_to_valve,
            self.useful_valves,
        ) = self.get_time_to_move_between_unblocked_valves(self.valves)
        self.best_so_far = BestSoFar()

    def solve_part_1(self):
        p = Progress(
            time_left=30,
            released_flow=0,
            current_flow_rate=0,
            visited=set(),
            to_visit={v for v in self.useful_valves if v != "AA"},
            current="AA",
        )
        self.visit(p)
        return max(f for f in self.best_so_far.values())

    def solve_part_2(self):
        p = Progress(
            time_left=26,
            released_flow=0,
            current_flow_rate=0,
            visited=set(),
            to_visit={v for v in self.useful_valves if v != "AA"},
            current="AA",
        )
        self.visit(p)
        max_combined = 0
        for i_open, ele_opens in itertools.combinations(self.best_so_far.keys(), 2):
            if set.isdisjoint(set(i_open), set(ele_opens)):
                comb = self.best_so_far[i_open] + self.best_so_far[ele_opens]
                max_combined = max(max_combined, comb)
        return max_combined

    def visit(self, p: Progress):
        no_more_to_visit = True
        for target in p.to_visit:
            time_needed = (
                self.time_to_valve[(p.current, target)] + TIME_TO_OPEN_ONE_VALVE
            )
            if p.time_left >= time_needed:
                no_more_to_visit = False
                candidate = p.visit(target, time_needed, self.valves)
                self.visit(candidate)
        if no_more_to_visit:
            self.best_so_far.add_from_progress(p.wait())

    @staticmethod
    def get_time_to_move_between_unblocked_valves(valves: dict[Location, Valve]):
        """Simplify graph. Only consider useful (initial and unblocked) valves.

        Calculate the times to get from any useful valve to any other
        useful valve.
        """
        adjacency_dict = {v.name: v.tunnels_to for v in valves.values()}
        G = nx.Graph(adjacency_dict)
        useful_valves = [v.name for v in valves.values() if v.flow_rate != 0]
        useful_valves.append("AA")
        time_to_valve = dict()
        for i, j in itertools.permutations(useful_valves, 2):
            time_to_get_there = len(nx.shortest_path(G, i, j)) - 1
            time_to_valve[(i, j)] = time_to_get_there
            time_to_valve[(j, i)] = time_to_get_there
        return time_to_valve, useful_valves


def part_1(inp):
    s = Solver(valves=inp)
    return s.solve_part_1()


def part_2(inp):
    s = Solver(valves=inp)
    return s.solve_part_2()


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
    self.assertEqual(1651, part_1(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
