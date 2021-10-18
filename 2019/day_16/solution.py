import itertools
from functools import lru_cache
from typing import List
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

def generate_repeating_pattern_batches(digit_number):
    repetitions = digit_number+1
    yield (0, repetitions - 1)
    yield from itertools.cycle(((1, repetitions), (0, repetitions), (-1, repetitions), (0, repetitions)))


def make_single_digit(signal_array):
    single_digit_signal = np.array([abs(num) % 10 for num in signal_array])
    return single_digit_signal

def make_singe_digit_iter(signal):
    yield from (abs(num) % 10 for num in signal)


def part_1_old(inp, num_phases=100):
    signal = np.array(inp)
    length = len(signal)
    pattern_matrix = np.stack(
        (np.fromiter(generate_repeating_pattern(row, length), 'int8', length) for row in range(length))
    )
    for _ in range(num_phases):
        output_signal = np.matmul(signal, pattern_matrix.T)
        output_signal_single_digit = make_single_digit(output_signal)
        signal = output_signal_single_digit
    return "".join([str(n) for n in signal[0:8]])

def full_signal_iter(inp, repetitions):
    for _ in range(repetitions):
        yield from inp

def generate_output_signal(signal, length):
    signal_orig = signal
    for row in range(length):
        signal_clone, signal_orig = itertools.tee(signal_orig)
        row_sum = 0
        for n, factor in zip(signal_clone, generate_repeating_pattern(row, length)):
            row_sum += n*factor
        yield row_sum

def generate_output_signal_in_batches(signal:List, length):
    print(f"input is of length {length}")
    for digit_number in range(length):
        #print(f"digit number is {digit_number}")
        digit_sum = 0
        pointer = 0
        for factor, quantity in generate_repeating_pattern_batches(digit_number):
            if factor == 1:
                digit_sum += sum(signal[pointer:pointer+quantity])
            elif factor == -1:
                digit_sum -= sum(signal[pointer:pointer+quantity])
            pointer += quantity
            if pointer > length:
                yield digit_sum
                break

def generate_output_signal_list(signal: List, length):
    # print(signal)
    output_signal = list()
    for digit_number in range(length):
        digit_sum = get_digit_sum(digit_number, length, signal)
        output_signal.append(abs(digit_sum) % 10)
    # print(output_signal)
    return output_signal

@lru_cache(None)
def generate_factors_array(digit_number, length):
    return np.fromiter(generate_repeating_pattern(digit_number, length), 'int8', length)

def part_2_with_trick(inp, repetitions=10000, num_phases=100):
    offset = int("".join([str(v) for v in inp[0:7]]))
    print(f"offset is {offset}")
    signal = list(full_signal_iter(inp, repetitions))
    length = len(signal)
    if not offset > length/2:
        raise RuntimeError("cannot use the trick")
    signal = signal[offset:]
    length = len(signal)
    for n in range(num_phases):
        print(f"phase {n}")
        output_list = [sum(signal)]
        for digit, value in zip(range(1, length), signal):
            digit_sum=output_list[-1]-value
            output_list.append(digit_sum)
        signal = [abs(v)%10 for v in output_list]

    return "".join([str(n) for n in signal[0:8]])

def generate_output_signal_array_mult_single(signal:List, length, offset):
    signal_array = np.array(signal)

    output_signal = list()
    for digit_number in range(length):
        if digit_number % 100 == 0:
            print(f"Calculating digit number {digit_number}")
        factors = np.fromiter(generate_repeating_pattern(digit_number, length), 'int8', length)
        scalar_product = np.dot(signal_array, factors)
        output_signal.append(abs(scalar_product) % 10)
    return output_signal

def get_digit_sum(digit_number, length, signal):
    digit_sum = 0
    signal_iter = iter(signal)
    counter = 0
    for _ in range(digit_number):
        # skip intial zeroes
        next(signal_iter)
        counter += 1
    while True:
        for _ in range(digit_number + 1):
            digit_sum += next(signal_iter)
            counter += 1
            if counter == length:
                return digit_sum
        for _ in range(digit_number + 1):
            next(signal_iter)
            counter += 1
            if counter == length:
                return digit_sum
        for _ in range(digit_number + 1):
            digit_sum -= next(signal_iter)
            counter += 1
            if counter == length:
                return digit_sum
        for _ in range(digit_number + 1):
            next(signal_iter)
            counter += 1
            if counter == length:
                return digit_sum



def part_1(inp, num_phases = 100):
    return part_2(inp, num_phases=num_phases, repetitions=1, is_part_1 = True)


def part_2(inp, num_phases = 100, repetitions = 10000, is_part_1=False):
    if not is_part_1:
        try:
            return part_2_with_trick(inp, repetitions=repetitions, num_phases=num_phases)
        except RuntimeError:
            pass
    offset = int("".join([str(v) for v in inp[0:7]]))
    print(f"offset is {offset}")
    signal = list(full_signal_iter(inp, repetitions))
    length = len(signal)
    for n in range(num_phases):
        print(f"phase {n}")
        output_signal = generate_output_signal_array_mult_single(signal, length, offset)
        signal = output_signal
    if is_part_1:
        return "".join([str(n) for n in signal[0:8]])
    return "".join([str(n) for n in signal[0:8]])


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

def test_sample_4(self):
    print("Part 2 test...")
    inp = [int(v) for v in "03036732577212944063491565474664"]
    expected = "84462026"
    self.assertEqual(expected, part_2(inp))

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_0(TestCase())
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    test_sample_3(TestCase())
    test_sample_4(TestCase())
    print('*** solving main ***')
    main("input")
