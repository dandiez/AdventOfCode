from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[char for char in line] for line in lines]  # parse here...
    return inp


def part_1(inp):
    return sum(get_parse_error_points(line) for line in inp)


char_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}

char_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def get_parse_error_points(line):
    stack = []
    for char in line:
        if is_valid_start(char):
            stack.append(char)
        else:
            expected_start = stack.pop()
            if char != char_pairs[expected_start]:
                return char_points[char]
    return 0

def is_valid_start(char):
    return char in char_pairs.keys()


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
    self.assertEqual(26397, part_1(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
