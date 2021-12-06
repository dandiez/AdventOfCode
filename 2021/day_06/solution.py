from collections import Counter, defaultdict
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines[0].split(',')]  # parse here...
    return inp


def part_1(inp):
    for n in range(80):
        inp = simulate_one(inp)
    return len(inp)


def simulate_one(inp):
    new_inp = []
    for f in inp:
        if f == 0:
            new_inp.append(6)
            new_inp.append(8)
        else:  #
            new_inp.append(f - 1)
    return new_inp


def part_2(inp):
    inp_dict = Counter(inp)
    for n in range(256):
        inp_dict = simulate_one_dict(inp_dict)
    return sum(inp_dict.values())


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
    # self.assertEqual(5934, part_1(inp))
    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
