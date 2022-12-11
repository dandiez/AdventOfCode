import dataclasses
import math
from typing import Iterable, Callable
from unittest import TestCase

MonkeyID = int


def read_input(filename="input"):
    with open(filename) as f:
        lines = f.read()
    raw_monkeys = [s.strip() for s in lines.split("\n\n") if s.strip()]
    monkeys = [Monkey.from_raw_string(s) for s in raw_monkeys]
    return monkeys


def get_operation_function(s: str) -> Callable[[int], int]:
    if s == "old * old":
        return lambda x: x * x
    elif "*" in s:
        return lambda x: x * int(s.split("*")[1])
    elif "+" in s:
        return lambda x: x + int(s.split("+")[1])
    raise ValueError("Cannot parse operation")


@dataclasses.dataclass
class Monkey:
    items: list
    operation: Callable[[int], int]
    test_mod: int
    true_monkey: int
    false_monkey: int
    num_inspected: int = 0

    @classmethod
    def from_raw_string(cls, s: str):
        lines = s.splitlines()
        items = [int(n.strip()) for n in lines[1][18:].split(",")]
        operation = get_operation_function(lines[2][18:].strip())
        test_mod = int(lines[3][21:].strip())
        true_monkey = int(lines[4][28:].strip())
        false_monkey = int(lines[5][29:].strip())
        return cls(items, operation, test_mod, true_monkey, false_monkey)

    def take_turn(self, worry_div) -> Iterable[tuple[int, MonkeyID]]:
        """Yield the item passed and the target monkey."""
        for item in self.items:
            old = item
            new = self.operation(old)
            if worry_div == 3:
                new = new // 3  # part 1
            else:
                new = new % worry_div  # part 2
            if new % self.test_mod == 0:
                yield new, self.true_monkey
            else:
                yield new, self.false_monkey
        self.num_inspected += len(self.items)
        self.items = []


@dataclasses.dataclass
class MonkeyPack:
    pack: list[Monkey]
    worry_div: int

    def play_round(self):
        for monkey in self.pack:
            new_items = monkey.take_turn(self.worry_div)
            for item, target in list(new_items):
                self.pack[target].items.append(item)

    def get_monkey_business_level(self):
        num_times = [m.num_inspected for m in self.pack]
        num_times.sort(reverse=True)
        return num_times[0] * num_times[1]


def part_1(inp):
    mp = MonkeyPack(inp, 3)
    for n in range(20):
        mp.play_round()
    return mp.get_monkey_business_level()


def part_2(inp):
    mp = MonkeyPack(inp, 1)
    mp.worry_div = math.prod(m.test_mod for m in mp.pack)
    for n in range(10000):
        mp.play_round()
    return mp.get_monkey_business_level()


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
    self.assertEqual(10605, part_1(inp))


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(2713310158, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
