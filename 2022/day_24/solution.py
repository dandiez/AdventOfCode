from __future__ import annotations

import dataclasses
from collections import deque
from itertools import count
from queue import Queue, PriorityQueue
from typing import Any
from unittest import TestCase

time: int
location: complex
direction: complex

UP = -1
DOWN = -UP
RIGHT = 1j
LEFT = -RIGHT
DIRS = {UP, DOWN, RIGHT, LEFT}


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


@dataclasses.dataclass
class Blizzard:
    start_loc: location
    direc: direction
    _known_locs: dict[time, location] = None

    def __post_init__(self):
        self._known_locs = {0: self.start_loc}

    def get_location_at_time(self, t: time, walls: set[location]):
        if t in self._known_locs:
            return self._known_locs[t]
        prev_time_loc = self._known_locs[t - 1]
        this_time_loc = prev_time_loc + self.direc
        if this_time_loc in walls:
            search_dir = -self.direc
            loc = this_time_loc + search_dir
            while loc not in walls:
                loc += search_dir
            loc -= search_dir
        else:
            loc = this_time_loc
        self._known_locs[t] = loc
        return loc


index = count(0)


@dataclasses.dataclass
class PrioritisedExpedition:
    prio: Any
    exp: Expedition

    def __lt__(self, other):
        return self.prio < other.prio


@dataclasses.dataclass(frozen=True)
class Expedition:
    loc: location
    t: t

    # previous_locations: list[location] = dataclasses.field(default_factory=list)

    def __hash__(self):
        return hash((self.t, self.loc))

    def prioritised(self) -> PrioritisedExpedition:
        """For the queue of expeditions to be explored.

        (use next(index) to ensure unique prio tuples)
        prio = time: bfs
        ...
        """
        return PrioritisedExpedition(prio=(self.t, next(index)), exp=self)
        # return PrioritisedExpedition(prio=(self.t - self.loc.real - self.loc.imag, next(index)), exp=self)
        # return PrioritisedExpedition(prio=(-self.t - self.loc.real - self.loc.imag, next(index)), exp=self)
        # return PrioritisedExpedition(prio=(self.t + self.loc.real + self.loc.imag, next(index)), exp=self)

    def next_loc(self, dest: location):
        return Expedition(loc=dest, t=self.t + 1, )  # previous_locations=self.previous_locations[:] + [self.loc])

    def wait(self):
        return Expedition(loc=self.loc, t=self.t + 1),  # previous_locations=self.previous_locations[:])


@dataclasses.dataclass
class Valley:
    blizzards: list[Blizzard]
    walls: set[location]
    start_location: location = None
    end_location: location = None
    blizzards_cache: dict[time, set[location]] = None

    def __post_init__(self):
        minx, *_, maxx = sorted(w.real for w in self.walls)
        miny, *_, maxy = sorted(w.imag for w in self.walls)
        self.start_location = minx + 1j
        self.end_location = maxx + maxy * 1j - 1j
        self.walls.add(self.start_location + UP)
        self.blizzards_cache = {0: set(b.get_location_at_time(0, self.walls) for b in self.blizzards)}

    @classmethod
    def from_raw(cls, lines: [str]):
        walls = set()
        blizzards = []
        for x, row in enumerate(lines):
            for y, char in enumerate(row):
                coords = x + 1j * y
                match char:
                    case ".":
                        continue
                    case "#":
                        walls.add(coords)
                    case ">":
                        blizzards.append(Blizzard(coords, RIGHT))
                    case "<":
                        blizzards.append(Blizzard(coords, LEFT))
                    case "^":
                        blizzards.append(Blizzard(coords, UP))
                    case "v":
                        blizzards.append(Blizzard(coords, DOWN))
                    case other:
                        raise ValueError(other)
        return cls(blizzards=blizzards, walls=walls)

    def update_blizzards_cache(self, t: time):
        if t in self.blizzards_cache:
            return
        self.blizzards_cache[t] = set(
            b.get_location_at_time(t, self.walls) for b in self.blizzards
        )

    def blizzs_at_time(self, t: time):
        if t not in self.blizzards_cache:
            self.update_blizzards_cache(t)
        return self.blizzards_cache[t]

    def find_best_time(self, start_time=0, backwards=False):
        if backwards:
            start_loc = self.end_location
            end_loc = self.start_location
        else:
            start_loc = self.start_location
            end_loc = self.end_location
        to_explore: PriorityQueue[PrioritisedExpedition] = PriorityQueue()
        exp = Expedition(loc=start_loc, t=start_time)
        to_explore.put(exp.prioritised())
        seen = set()
        best = None
        while len(to_explore.queue) > 0:
            prio_exp = to_explore.get()
            exp = prio_exp.exp
            # if exp.t > depth:
            #    print(exp.t, len(to_explore.queue), len(seen))
            #    depth = exp.t
            if exp.loc == end_loc:
                if best is None:
                    best = exp
                elif best.t > exp.t:
                    best = exp
            for dest in (exp.loc + d for d in (*DIRS, 0)):
                if dest in self.walls:
                    continue
                if dest in self.blizzs_at_time(exp.t + 1):
                    continue
                next_state = exp.next_loc(dest)
                if next_state in seen:
                    continue
                if best is not None and next_state.t > best.t:
                    continue
                seen.add(next_state)
                to_explore.put(next_state.prioritised())
        return best.t

    def show(self, t: time, expedition: location):
        minx, *_, maxx = sorted(w.real for w in self.walls)
        miny, *_, maxy = sorted(w.imag for w in self.walls)
        s = []
        for x in range(round(minx), round(maxx) + 1):
            for y in range(round(miny), round(maxy) + 1):
                c = x + 1j * y
                if c in self.walls:
                    s.append("#")
                elif c in self.blizzs_at_time(t):
                    s.append("@")
                elif c == expedition:
                    s.append("E")
                else:
                    s.append(".")
            s.append("\n")
        print("".join(s))


def part_1(inp):
    v = Valley.from_raw(inp)
    return v.find_best_time()


def part_2(inp):
    v = Valley.from_raw(inp)
    leg1_t = v.find_best_time()
    leg2_t = v.find_best_time(start_time=leg1_t, backwards=True)
    leg3_t = v.find_best_time(start_time=leg2_t)
    return leg3_t


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
    self.assertEqual(18, part_1(inp))
    pass


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(54, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
