import copy
import itertools
from collections import deque
from unittest import TestCase

from day_05.solution import IntcodeComputer


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


def read_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines[0].split(",")  # parse here...
    inp = [int(v) for v in inp]
    return inp


def part_1(inp):
    max_second_input = 0
    for phase_combo in itertools.permutations(range(5)):
        amplifiers = [Amplifier(copy.deepcopy(inp), phase) for phase in phase_combo]
        second_input = 0
        for amplifier in amplifiers:
            amplifier.set_second_input(second_input)
            amplifier.computer.execute()
            second_input = amplifier.get_output()
        max_second_input = max(max_second_input, second_input)
    return max_second_input


def part_2(inp):
    max_second_input = 0
    for phase_combo in itertools.permutations(range(5, 10)):
        amplifiers = [Amplifier(copy.deepcopy(inp), phase) for phase in phase_combo]
        signal = 0
        last_computer = amplifiers[-1].computer
        while last_computer.is_paused==True or last_computer.stop==False:
            for amplifier in amplifiers:
                amplifier.set_second_input(signal)
                amplifier.computer.execute()
                signal = amplifier.get_output()
            max_second_input = max(max_second_input, signal)
    return max_second_input

class Amplifier:

    def __init__(self, memory, phase):
        self.computer = IntcodeComputer(memory)
        self.computer.input = deque([phase])

    def set_second_input(self, second_input):
        self.computer.input.append(second_input)

    def get_output(self):
        return self.computer.outputs[-1]



def test_sample_1(self):
    inp = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    self.assertEqual(43210, part_1(inp))


def test_sample_2(self):
    inp = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
           101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    self.assertEqual(54321, part_1(inp))


def test_sample_3(self):
    inp = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
           1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    self.assertEqual(65210, part_1(inp))

def test_sample_4(self):
    inp = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    self.assertEqual(139629729, part_2(inp))

def test_sample_5(self):
    inp = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    self.assertEqual(18216, part_2(inp))

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    test_sample_3(TestCase())
    test_sample_4(TestCase())
    test_sample_5(TestCase())
    print('*** solving main ***')
    main("input")
