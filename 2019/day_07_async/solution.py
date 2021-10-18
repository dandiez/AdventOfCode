import asyncio
import copy
import itertools
import operator
from asyncio import queues
from collections import deque
from enum import Enum
from unittest import TestCase


class Modes(Enum):
    POSITION = 0
    IMMEDIATE = 1


class Code:

    def __init__(self, code_raw: int):
        self.op_code = code_raw % 100
        modes_str = str(code_raw // 100)[::-1]
        self.modes = {n: Modes(int(mode_str)) for n, mode_str in enumerate(modes_str)}

    def get_n_mode(self, n: int):
        return self.modes.get(n, Modes.POSITION)


class IntcodeComputer:

    def __init__(self, memory, name=None):
        self.memory = memory
        self.position = 0
        self.max_cycles = 1000000
        self.stop = False
        self.input_queue = queues.Queue()
        self.output_queue = queues.Queue()
        self.last_output = None
        self.name = name or ''

    def read_and_skip(self):
        value = self.memory[self.position]
        self.position += 1
        return value

    async def execute(self):
        self.stop = False
        num_cycles = 0
        while num_cycles <= self.max_cycles and not self.stop:
            await self.process_instruction()
            num_cycles += 1
        if num_cycles >= self.max_cycles:
            raise RecursionError("Reached max cycles.")

    async def process_instruction(self):
        code_raw = self.read_and_skip()
        code = Code(code_raw)
        if code.op_code == 1:
            self.process_sum(code)
        elif code.op_code == 2:
            self.process_mul(code)
        elif code.op_code == 3:
            await self.process_consume_input(code)
        elif code.op_code == 4:
            await self.process_write_output(code)
        elif code.op_code == 5:
            self.process_jump_if_true(code)
        elif code.op_code == 6:
            self.process_jump_if_false(code)
        elif code.op_code == 7:
            self.process_less_than(code)
        elif code.op_code == 8:
            self.process_equal(code)
        elif code.op_code == 99:
            self.stop = True
        else:
            raise ValueError(f"Unknown code {code.op_code}")

    def process_less_than(self, code):
        self.process_two_input_function(code, lambda a, b: int(operator.lt(a, b)))

    def process_equal(self, code):
        self.process_two_input_function(code, lambda a, b: int(operator.eq(a, b)))

    def process_sum(self, code):
        self.process_two_input_function(code, operator.add)

    def process_mul(self, code):
        self.process_two_input_function(code, operator.mul)

    def process_jump_if_true(self, code):
        first, second = self.read_n_parameter_values(code, 2)
        if first != 0:
            self.position = second

    def process_jump_if_false(self, code):
        first, second = self.read_n_parameter_values(code, 2)
        if first == 0:
            self.position = second

    async def process_consume_input(self, code):
        value_to_consume = await self.input_queue.get()
        # print(f'{self.name}: consuming input {value_to_consume}')
        self.memory[self.read_and_skip()] = value_to_consume

    async def process_write_output(self, code):
        value = self.read_n_parameter_values(code, 1)[0]
        # print(f'{self.name}: output: {value}')
        self.last_output = value
        await self.output_queue.put(value)

    def process_two_input_function(self, code, f: callable):
        params = self.read_n_parameter_values(code, 2)
        output_address = self.read_and_skip()
        self.memory[output_address] = f(*params)

    def read_n_parameter_values(self, code: Code, number_of_parameter_values_to_get: int):
        values = []
        for n in range(number_of_parameter_values_to_get):
            mode_n = code.get_n_mode(n)
            if mode_n is Modes.POSITION:
                values.append(self.memory[self.read_and_skip()])
            else:
                values.append(self.read_and_skip())
        return values


async def part_1(inp, phases=None, link_function=None):
    """Solve part 1 with default arguments and part 2 with the right phases and link_function

    :param inp: memory list
    :param phases: allowed phases to assign to the amplifiers
    :param link_function: function that links amplifiers together
    :return: solution
    """
    num_amplifiers = 5

    # inputs default to part 1
    phases = phases or range(num_amplifiers)
    link_function = link_function or link_amplifiers_part_1

    max_second_input = 0
    for phase_combo in itertools.permutations(phases):
        amplifiers = await instantiate_amplifiers(inp, num_amplifiers)
        await link_function(amplifiers, num_amplifiers)
        await set_phase(amplifiers, phase_combo)
        await amplifiers[0].input_queue.put(0)
        tasks = await create_amplifier_tasks(amplifiers)
        await tasks[-1]
        signal = await get_final_output_from_last_amplifier(amplifiers)
        max_second_input = max(max_second_input, signal)
    return max_second_input


async def get_final_output_from_last_amplifier(amplifiers):
    signal = amplifiers[-1].last_output
    # The last amplifier could end the program, but the first amplifier might consume
    #  the last output. Therefore store it in .last_output.
    # The check below should pass if the first amplifier also ended the program (not guaranteed).
    assert signal == await amplifiers[-1].output_queue.get()
    return signal


async def instantiate_amplifiers(inp, num_amplifiers):
    return [IntcodeComputer(copy.deepcopy(inp), name=f'comp {n}') for n in range(num_amplifiers)]


async def set_phase(amplifiers, phase_combo):
    for amplifier, phase in zip(amplifiers, phase_combo):
        await amplifier.input_queue.put(phase)


async def create_amplifier_tasks(amplifiers):
    tasks = [asyncio.create_task(amplifier.execute()) for amplifier in amplifiers]
    return tasks


async def link_amplifiers_part_2(amplifiers, num_amplifiers):
    for id in range(num_amplifiers):
        amplifiers[id].input_queue = amplifiers[(id - 1) % num_amplifiers].output_queue


async def link_amplifiers_part_1(amplifiers, num_amplifiers):
    for id in range(1, num_amplifiers):
        amplifiers[id].input_queue = amplifiers[id - 1].output_queue


async def part_2(inp):
    return await part_1(inp, range(5, 10), link_amplifiers_part_2)


def read_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines[0].split(",")  # parse here...
    inp = [int(v) for v in inp]
    return inp


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = asyncio.run(part_1(inp))
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = asyncio.run(part_2(inp))
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    inp = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    self.assertEqual(43210, asyncio.run(part_1(inp)))
    print('Sample 1 done')


def test_sample_2(self):
    inp = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
           101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    self.assertEqual(54321, asyncio.run(part_1(inp)))
    print('Sample 2 done')


def test_sample_3(self):
    inp = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
           1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    self.assertEqual(65210, asyncio.run(part_1(inp)))
    print('Sample 3 done')


def test_sample_4(self):
    inp = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
           27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
    self.assertEqual(139629729, asyncio.run(part_2(inp)))
    print('Sample 4 done')

def test_sample_5(self):
    inp = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
           -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
           53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
    self.assertEqual(18216, asyncio.run(part_2(inp)))
    print('Sample 5 done')

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    test_sample_3(TestCase())
    test_sample_4(TestCase())
    test_sample_5(TestCase())
    print('*** solving main ***')
    main("input")
