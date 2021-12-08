import itertools
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
    return sum(get_number(line) for line in inp)


segment_map = {
    (0, 1, 2, 3, 5, 6): 0,
    (3, 6): 1,
    (0, 1, 3, 4, 5): 2,
    (0, 1, 3, 4, 6): 3,
    (2, 3, 4, 6): 4,
    (0, 1, 2, 4, 6): 5,
    (0, 1, 2, 4, 5, 6): 6,
    (1, 3, 6): 7,
    (0, 1, 2, 3, 4, 5, 6): 8,
    (0, 1, 2, 3, 4, 6): 9,
}


def get_number(line):
    ten, four = line
    for perm in itertools.permutations('abcdefg'):
        key = {letter: segment for segment, letter in enumerate(perm)}
        try:
            decode_all(ten, key)
        except ValueError:
            continue
        else:
            return decode_four(four, key)


def decode(str_num, key ):
    segments = []
    for digit in str_num:
        segments.append(key[digit])
    segs = tuple(sorted(segments))
    if tuple(sorted(segments)) in segment_map:
        return segment_map[segs]
    raise ValueError('not possible')

def decode_four(four, key):
    decoded = [decode(str_num, key) for str_num in four]
    return decoded[0]*1000+decoded[1]*100+decoded[2]*10+decoded[3]


def decode_all(ten, key):
    for num in ten:
        decode(num, key)


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
    self.assertEqual(61229, part_2(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
