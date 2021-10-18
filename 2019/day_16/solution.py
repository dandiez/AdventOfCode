import itertools
from unittest import TestCase

import numpy as np


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


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines[0]]  # parse here...
    return inp


def generate_base_cyclic_pattern_for_row(row):
    base_pattern = (0, 1, 0, -1)
    repeat_times = row + 1
    for value in itertools.cycle(base_pattern):
        for _ in range(repeat_times):
            yield value


def generate_repeating_pattern(row, length):
    base = generate_base_cyclic_pattern_for_row(row)
    next(base)  # consume first element
    value = next(base)
    for _ in range(length):
        yield value
        value = next(base)


def make_single_digit(signal_array):
    single_digit_signal = np.array([abs(num) % 10 for num in signal_array])
    return single_digit_signal


def part_1(inp, num_phases=100):
    signal = np.array(inp)
    length = len(signal)
    pattern_matrix = np.array([list(generate_repeating_pattern(row, length)) for row in range(length)])
    for _ in range(num_phases):
        output_signal = np.matmul(signal, pattern_matrix.T)
        output_signal_single_digit = make_single_digit(output_signal)
        signal = output_signal_single_digit
    return "".join([str(n) for n in signal[0:8]])


def part_2(inp):
    pass


def test_sample_0(self):
    inp = [int(v) for v in "12345678"]
    expected = "01029498"
    self.assertEqual(expected, part_1(inp, num_phases=4))


def test_sample_1(self):
    inp = [int(v) for v in "80871224585914546619083218645595"]
    expected = "24176176"
    self.assertEqual(expected, part_1(inp))


def test_sample_2(self):
    inp = [int(v) for v in "19617804207202209144916044189917"]
    expected = "73745418"
    self.assertEqual(expected, part_1(inp))


def test_sample_3(self):
    inp = [int(v) for v in "69317163492948606335995924319873"]
    expected = "52432133"
    self.assertEqual(expected, part_1(inp))


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_0(TestCase())
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    test_sample_3(TestCase())
    print('*** solving main ***')
    main("input")
