from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    lines = [line.split(" ") for line in lines]  # parse here...
    return lines

def get_x(inp):
    x = 1
    yield x
    for line in inp:
        if line[0] == "noop":
            yield x
        elif line[0] == "addx":
            yield x
            x += int(line[1])
            yield x
    yield x

def part_1(inp):
    signal_strength = 0
    key_cycles = [n+19 for n in range(300) if not n % 40]
    for n, x in enumerate(get_x(inp)):
        if n in key_cycles:
            N=n+1
            sigstr = x*N
            print(f"N: {N}, x: {x}, sigstr: {sigstr}")
            signal_strength += sigstr
    return signal_strength


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
    self.assertEqual(13140, part_1(inp))
    pass


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
