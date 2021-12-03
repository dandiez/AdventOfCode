from unittest import TestCase

import numpy as np


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [val for val in lines]  # parse here...
    return inp

def list_to_bin(a_list):
    numstr = ''.join([str(d) for d in a_list])
    return int(numstr, 2)

def part_1(inp):
    print(inp)
    num_total = len(inp)
    num_arrays = [np.array([int(digit) for digit in num]) for num in inp]
    print(num_arrays)
    sum_nums = sum(num_arrays)
    print(sum_nums)
    mid_number = num_total // 2
    gamma = []
    epsilon = []
    for digit in sum_nums:
        if digit > mid_number:
            gamma.append(1)
            epsilon.append(0)
        else:
            gamma.append(0)
            epsilon.append(1)
    return list_to_bin(gamma)*list_to_bin(epsilon)

    pass

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
    self.assertEqual(198, part_1(inp))
    pass

def test_sample_2(self):
    pass

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
