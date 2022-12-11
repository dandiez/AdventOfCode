import dataclasses
from unittest import TestCase

from typing_extensions import Literal


def read_input(filename="input"):
    with open(filename) as f:
        lines = f.read()
    raw_monkeys =[s.strip() for s in lines.split("\n\n") if s.strip()]
    monkeys = [Monkey.from_raw_string(s) for s in raw_monkeys]
    return monkeys




@dataclasses.dataclass
class Monkey:
    items: list
    operation: str
    test_mod: int
    true_monkey: int
    false_monkey: int
    num_inspected: int = 0

    @classmethod
    def from_raw_string(cls, s: str):
        lines = s.splitlines()
        items = [int(n.strip()) for n in lines[1][18:].split(",")]
        operation = lines[2][18:].strip()
        test_mod = int(lines[3][21:].strip())
        true_monkey = int(lines[4][28:].strip())
        false_monkey = int(lines[5][29:].strip())
        return cls(items, operation, test_mod,true_monkey,false_monkey)

    def take_turn(self, worry_div):
        for item in self.items:
            old = item
            new = eval(self.operation)
            if worry_div == 3:
                new = new // 3
            else:
                new = new % worry_div
            if new % self.test_mod ==0:
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
                print(f"Thrown {item} to {target}")
                self.pack[target].items.append(item)



def part_1(inp):
    mp = MonkeyPack(inp, 3)
    for n in range(20):
        mp.play_round()
        print(mp)
    num_times = [m.num_inspected for m in mp.pack]
    num_times = sorted(num_times, reverse=True)
    return num_times[0]*num_times[1]

def part_2(inp):
    mp = MonkeyPack(inp, 1)
    w = 1
    for m in mp.pack:
        w *= m.test_mod
    mp.worry_div = w
    for n in range(10000):
        mp.play_round()
        print(mp)
    num_times = [m.num_inspected for m in mp.pack]
    num_times = sorted(num_times, reverse=True)
    return num_times[0] * num_times[1]


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
    pass


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(2713310158, part_2(inp))
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
