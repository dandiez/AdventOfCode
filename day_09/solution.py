import asyncio
import operator
from asyncio import queues
from collections import defaultdict
from enum import Enum
from unittest import TestCase


class Modes(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Code:

    def __init__(self, code_raw: int):
        self.op_code = code_raw % 100
        modes_str = str(code_raw // 100)[::-1]
        self.modes = {n: Modes(int(mode_str)) for n, mode_str in enumerate(modes_str)}

    def get_n_mode(self, n: int):
        return self.modes.get(n, Modes.POSITION)


class IntcodeComputer:

    def __init__(self, memory, name=None):
        self.memory = self.memory_as_dict(memory)
        self.position = 0
        self.max_cycles = 1000000
        self.stop = False
        self.input_queue = queues.Queue()
        self.output_queue = queues.Queue()
        self.last_output = None
        self.name = name or ''
        self.relative_base = 0
        self.paused = False

    @staticmethod
    def memory_as_dict(memory):
        dict_memory = defaultdict(int)
        for k, v in enumerate(memory):
            dict_memory[k] = v
        return dict_memory

    def read_and_skip(self):
        value = self.memory[self.position]
        self.position += 1
        return value

    async def execute(self):
        self.stop = False
        self.paused = False
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
        elif code.op_code == 9:
            self.process_adjust_relative_base(code)
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
        if self.input_queue.empty():
            self.paused = True
            self.stop = True
            self.position -= 1
            return
        value_to_set = await self.input_queue.get()
        # print(f'{self.name}: consuming input {value_to_consume}')
        output_mode = code.get_n_mode(0)
        self.set_memory_based_on_mode(output_mode, value_to_set)

    def set_memory_based_on_mode(self, output_mode, value_to_set):
        if output_mode is Modes.POSITION:
            self.memory[self.read_and_skip()] = value_to_set
        elif output_mode is Modes.RELATIVE:
            self.memory[self.read_and_skip() + self.relative_base] = value_to_set

    async def process_write_output(self, code):
        value = self.read_n_parameter_values(code, 1)[0]
        # print(f'{self.name}: output: {value}')
        self.last_output = value
        await self.output_queue.put(value)

    def process_adjust_relative_base(self, code):
        value = self.read_n_parameter_values(code, 1)[0]
        self.relative_base += value

    def process_two_input_function(self, code, f: callable):
        params = self.read_n_parameter_values(code, 2)
        value_to_set = f(*params)
        output_mode = code.get_n_mode(2)
        self.set_memory_based_on_mode(output_mode, value_to_set)

    def read_n_parameter_values(self, code: Code, number_of_parameter_values_to_get: int):
        values = []
        for n in range(number_of_parameter_values_to_get):
            mode_n = code.get_n_mode(n)
            if mode_n is Modes.POSITION:
                values.append(self.memory[self.read_and_skip()])
            elif mode_n is Modes.IMMEDIATE:
                values.append(self.read_and_skip())
            elif mode_n is Modes.RELATIVE:
                values.append(self.memory[self.read_and_skip() + self.relative_base])
            else:
                raise ValueError(f'Unknown mode {mode_n}')
        return values

    def execution_ended(self):
        return self.stop and not self.paused

def part_1(inp):
    p1 = asyncio.run(main_event_loop(inp, start_value=1))
    return p1


async def main_event_loop(inp, start_value=None):
    comp = IntcodeComputer(inp)
    if start_value is not None:
        await comp.input_queue.put(start_value)
    await comp.execute()
    q = comp.output_queue
    p1 = [await q.get() for _ in range(q.qsize())]
    return p1


def part_2(inp):
    p2 = asyncio.run(main_event_loop(inp, start_value=2))
    return p2


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
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = part_2(inp)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    inp = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    self.assertEqual(inp, part_1(inp))
    print('Sample 1 done')


def test_sample_2(self):
    inp = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    self.assertEqual(16, len(str(part_1(inp)[0])))
    print('Sample 2 done')


def test_sample_3(self):
    inp = [104, 1125899906842624, 99]
    self.assertEqual([1125899906842624], part_1(inp))
    print('Sample 3 done')


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    test_sample_3(TestCase())
    print('*** solving main ***')
    main("input")
