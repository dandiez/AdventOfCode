
from unittest import TestCase

def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(p1)

    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(p2)
    return p1, p2


def read_input(filename="input.txt"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines]  # parse here...
    return inp


def part_1(inp):
    pass


def part_2(inp):
    pass



def test_sample_1(self):
    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    main("input")
