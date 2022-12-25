from __future__ import annotations

import dataclasses
import re
from enum import Enum
from math import prod
from queue import Queue, PriorityQueue, LifoQueue
from typing import Iterable
from unittest import TestCase

from aoc_utils.vectors.tupvec_int import Vint as V


class Material(Enum):
    ore = 0
    clay = 1
    obsidian = 2
    open_geode = 3


class Mats(V):
    @classmethod
    def from_dict(cls, mats: dict[Material, int]):
        return cls([mats[m] if m in mats else 0 for m in Material])

    def __ge__(self, other):
        return all(a >= b for a, b in zip(self, other, strict=True))

    def __gt__(self, other):
        return all(a > b for a, b in zip(self, other, strict=True))

    @staticmethod
    def max_any(mats: Iterable[Mats]):
        return Mats(max(*ab) for ab in zip(*mats, strict=True))


@dataclasses.dataclass
class RobotType:
    cost: Mats
    prod_per_min: Mats


@dataclasses.dataclass()
class Blueprint:
    id: int
    robot_types: list[RobotType]
    max_any: Mats = None

    def __post_init__(self):
        self.max_any = self.max_cost_any_mat()

    @classmethod
    def from_ints(cls, n: list[int]):
        return cls(
            id=n[0],
            robot_types=[
                RobotType(
                    cost=Mats(n[5], 0, n[6], 0),
                    prod_per_min=Mats.from_dict({Material.open_geode: 1}),
                ),
                RobotType(
                    cost=Mats(n[3], n[4], 0, 0),
                    prod_per_min=Mats.from_dict({Material.obsidian: 1}),
                ),
                RobotType(
                    cost=Mats(n[2], 0, 0, 0),
                    prod_per_min=Mats.from_dict({Material.clay: 1}),
                ),
                RobotType(
                    cost=Mats(n[1], 0, 0, 0),
                    prod_per_min=Mats.from_dict({Material.ore: 1}),
                ),
            ],
        )

    def max_cost_any_mat(self):
        mx = Mats.max_any(b.cost for b in self.robot_types)
        mx += Mats.from_dict({Material.open_geode: 9e99})
        return mx


def get_numbers_from_string(s: str):
    return [
        int(s)
        for s in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", s)
    ]


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    integers = [get_numbers_from_string(val) for val in lines]  # parse here...
    bps = [Blueprint.from_ints(ints) for ints in integers]
    return bps


@dataclasses.dataclass(frozen=True)
class Factory:
    ores: Mats
    prod_per_min: Mats
    time_left: int

    def next_states(self, blueprint: Blueprint) -> Iterable[Factory]:
        if self.time_left == 0:
            return []
        new_states = []
        for robot_type in blueprint.robot_types:
            new_f = self.build(robot_type)
            if new_f is not None:
                if any(pr > maxpr for pr, maxpr in zip(new_f.prod_per_min, blueprint.max_any)):
                    # print(f"New prod would be {new_f.prod_per_min}. Max ever needed is {blueprint.max_any}")
                    continue
                new_states.append(new_f)
        if not new_states:
            f = Factory(ores=self.ores + self.prod_per_min * self.time_left,
                        prod_per_min=self.prod_per_min,
                        time_left=0)
            if f.ores[Material.open_geode.value] != 0:
                # print(f"Cashing in {f}")
                return [f]
            return []
        else:
            return new_states

    def build(self, robot_type: RobotType):
        mats_needed = robot_type.cost - self.ores
        current_prod = self.prod_per_min
        try:
            time_per_mat = [max(-(m // -c), 0) if m != 0 else 0 for m, c in zip(mats_needed, current_prod)]
        except ZeroDivisionError:
            return
        time_to_wait = max(time_per_mat) + 1
        if time_to_wait >= self.time_left:
            return
        f = Factory(ores=self.ores + self.prod_per_min * time_to_wait - robot_type.cost,
                    prod_per_min=self.prod_per_min + robot_type.prod_per_min,
                    time_left=self.time_left - time_to_wait
                    )
        return f

    def priority(self):

        # ore_value = Mats(1, 10, 100, 1000).dot(self.ores)
        production_value = (
            Mats(1, 10, 100, 1000).dot(self.prod_per_min)
        )
        # return self.time_left
        return -production_value


class BestSoFar(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_open = 0

    def register(self, f: Factory):
        self.add(f)
        opge = f.ores[Material.open_geode.value]
        if opge > self.max_open:
            print(opge)
            self.max_open = opge


@dataclasses.dataclass(frozen=True)
class FactoryWithPrio:
    factory: Factory
    prio: int

    @classmethod
    def from_factory(cls, f: Factory):
        return cls(f, prio=f.priority())

    def __lt__(self, other):
        return (self.prio,) < (other.prio,)


@dataclasses.dataclass
class QualityFinder:
    blueprint: Blueprint
    seen: BestSoFar

    def find_quality(self, starting_factory: Factory):
        return self.blueprint.id * self.find_most_ores(starting_factory)

    def find_most_ores(self, starting_factory: Factory):
        to_see = PriorityQueue()
        to_see.put(FactoryWithPrio.from_factory(starting_factory))
        self.seen.register(starting_factory)
        while not to_see.empty():
            f = to_see.get().factory
            options = f.next_states(self.blueprint)
            for next_f in options:
                if next_f in self.seen:
                    continue
                self.seen.register(next_f)
                to_see.put(FactoryWithPrio.from_factory(next_f))
        return self.seen.max_open


def part_2(inp):
    return prod(QualityFinder(blueprint=b, seen=BestSoFar()).find_most_ores(
        Factory(
            ores=Mats(0, 0, 0, 0),
            prod_per_min=Mats.from_dict({Material.ore: 1}),
            time_left=32,
        )
    ) for b in inp[:3])


def part_1(inp):
    return sum(
        QualityFinder(blueprint=b, seen=BestSoFar()).find_quality(
            Factory(
                ores=Mats(0, 0, 0, 0),
                prod_per_min=Mats.from_dict({Material.ore: 1}),
                time_left=24,
            )
        )
        for b in inp
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
    # print(inp[0])
    # q = QualityFinder(blueprint=inp[0], seen=BestSoFar()).find_quality(
    #     Factory(
    #         ores=Mats(0, 0, 0, 0),
    #         prod_per_min=Mats.from_dict({Material.ore: 1}),
    #         time_left=24,
    #     )
    # )
    # self.assertEqual(9, q)
    self.assertEqual(33, part_1(inp))
    pass


def test_sample_2(self):
    # inp = read_input("sample_1")
    # self.assertEqual(1, part_1(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    # test_sample_1(TestCase())
    # test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
