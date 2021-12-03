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

def keep(char, position, numbers):
    to_keep = []
    for num in numbers:
        if num[position]==char:
            to_keep.append(num)
    return to_keep

def most_common(inp, oxy=True):
    remaining = inp[:]
    digit = 0
    while len(remaining)>1:
        num_ones = 0
        num_zeroes = 0
        for num in remaining:
            if num[digit]=='1':
                num_ones+=1
            else:
                num_zeroes+=1
        if oxy:
            if num_ones>= num_zeroes:
                remaining=keep('1', digit, remaining)
            else:
                remaining=keep('0', digit, remaining)
        else:
            if num_zeroes <= num_ones:
                remaining=keep('0', digit, remaining)
            else:
                remaining=keep('1', digit, remaining)
        digit+=1
    return int(remaining[0], 2)

def part_2(inp):
    ox = most_common(inp, True)
    co2 = most_common(inp, False)
    return ox*co2

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
    self.assertEqual(230, part_2(inp))
    pass

def test_sample_2(self):
    pass

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
