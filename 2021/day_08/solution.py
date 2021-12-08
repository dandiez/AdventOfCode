from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [parse_line(line) for line in lines]  # parse here...
    return inp

def parse_line(line):
    left, right = line.split('|')
    ten_digits = [val.strip() for val in left.split()]
    four_digits = [val.strip() for val in right.split()]
    return ten_digits, four_digits

def part_1(inp):
    print(inp)
    count = 0
    for ten, four in inp:
        for number in four:
            if len(number) in [2, 4, 3, 7]:
                count += 1
    return count

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
    self.assertEqual(26, part_1(inp))


def test_sample_2(self):
    pass

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
