import dataclasses
import itertools
from functools import lru_cache
from typing import Iterable
from unittest import TestCase
import networkx as nx

Location = str


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
    return [Valve.from_str(line) for line in lines]


@dataclasses.dataclass(frozen=True)
class State:
    location: str
    minutes_left: int
    open_valves: tuple[bool]


TIME_TO_OPEN_ONE_VALVE = 1


@dataclasses.dataclass(frozen=True)
class Map:
    locations: tuple[Location]
    flow_rates: tuple[int]
    time_to_valve: tuple[tuple[Location, Location], int]

    @lru_cache(None)
    def valves_that_can_be_opened_on_time(self, state) -> Iterable[Location]:
        time_available = state.minutes_left - TIME_TO_OPEN_ONE_VALVE
        closed_valves = [
            v
            for v, isopen in zip(map.locations, state.open_valves)
            if not isopen and v != state.location
        ]
        for v in closed_valves:
            if self.time_to_reach_valve(state.location, v) <= time_available:
                yield v

    def flow_rate_at_visited(self, visited: tuple[bool]) -> int:
        """Total flow rate produced by visited locations in one minute."""
        return sum(f for f, v in zip(self.flow_rates, visited) if v)

    def is_open(self, state: State, loc):
        return state.open_valves[self.locations.index(loc)]

    def open_valve_at_loc(self, currently_open: tuple[bool], loc: Location):
        new_open = []
        for current, _loc in zip(currently_open, self.locations):
            if _loc == loc:
                new_open.append(True)
            else:
                new_open.append(current)
        return tuple(new_open)

    @lru_cache(None)
    def time_to_reach_valve(self, from_v: Valve, to_v: Valve):
        for from_to, time in self.time_to_valve:
            if from_to == (from_v, to_v):
                return time
        raise KeyError(from_v, to_v)


@lru_cache(None)
def find_max_pressure(state: State) -> int:

    global map
    total_flow_released = 0
    if state.minutes_left == 0:
        return total_flow_released
    current_flow_per_minute = map.flow_rate_at_visited(state.open_valves)
    # There is till time, so we can...
    # wait here for "minute_left" minutes...
    max_flows = [current_flow_per_minute*state.minutes_left]

    # if the current valve is closed we can open it...
    if not map.is_open(state, state.location):
        max_flows.append(
            find_max_pressure(
                State(
                    location=state.location,
                    minutes_left=state.minutes_left - TIME_TO_OPEN_ONE_VALVE,
                    open_valves=map.open_valve_at_loc(
                        state.open_valves, state.location
                    ),
                )
            )
            + current_flow_per_minute * TIME_TO_OPEN_ONE_VALVE
        )
    # and we can move to a location that still has a closed valve.
    for new_loc in map.valves_that_can_be_opened_on_time(state):
        time_to_reach = map.time_to_reach_valve(state.location, new_loc)
        max_flows.append(
            find_max_pressure(
                State(
                    location=new_loc,
                    minutes_left=state.minutes_left - time_to_reach,
                    open_valves=state.open_valves,
                )
            )
            + time_to_reach * current_flow_per_minute
        )
    return max(max_flows)


def part_1(inp: list[Valve]):
    valves: dict[Location, Valve] = {v.name: v for v in inp}
    time_to_valve, useful_valves = get_time_to_move_between_unblocked_valves(valves)

    global map
    map = Map(
        locations=tuple(useful_valves),
        flow_rates=tuple(valves[v].flow_rate for v in useful_valves),
        time_to_valve=tuple(time_to_valve.items()),
    )
    state = State(
        location="AA",
        minutes_left=30,
        open_valves=tuple(False for v in useful_valves),
    )
    return find_max_pressure(state)


def get_time_to_move_between_unblocked_valves(valves):
    adjacency_dict = {v.name: v.tunnels_to for v in valves.values()}
    G = nx.Graph(adjacency_dict)
    unblocked_valves = [v.name for v in valves.values() if v.flow_rate != 0]
    unblocked_valves.append("AA")
    time_to_valve = dict()
    for i, j in itertools.product(unblocked_valves, repeat=2):
        if i == j:
            continue
        time_to_get_there = len(nx.shortest_path(G, i, j)) - 1
        time_to_valve[(i, j)] = time_to_get_there
        time_to_valve[(j, i)] = time_to_get_there
    return time_to_valve, unblocked_valves


def part_2(inp):
    pass


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
    find_max_pressure.cache_clear()
    Map.valves_that_can_be_opened_on_time.cache_clear()
    Map.time_to_reach_valve.cache_clear()


def test_sample_2(self):
    # inp = read_input("sample_1")
    # self.assertEqual(1, part_1(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
