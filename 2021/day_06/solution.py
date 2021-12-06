from collections import Counter, defaultdict
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines[0].split(',')]  # parse here...
    return inp


def part_1(inp):
    return simulate_many(inp, 80)


def part_2(inp):
    return simulate_many(inp, 256)


def simulate_many(inp, cycles):
    inp = Counter(inp)
    for n in range(cycles):
        inp = simulate_one_dict(inp)
    return sum(inp.values())


def simulate_one_dict(inp):
    new_inp = defaultdict(int)
    for k, v in inp.items():
        if k == 0:
            new_inp[8] += v
            new_inp[6] += v
        else:
            new_inp[k - 1] += v
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
    self.assertEqual(5934, part_1(inp))


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    print('*** solving main ***')
    main("input")
