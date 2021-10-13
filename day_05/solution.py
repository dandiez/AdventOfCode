import operator
from enum import Enum


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp, 1)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = part_1(inp, 5)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def part_1(inp, inp_value):
    computer = IntcodeComputer(inp)
    computer.set_input(inp_value)
    computer.execute()
    p_1 = computer.outputs[-1]
    return p_1


def read_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines[0].split(",")  # parse here...
    inp = [int(v) for v in inp]
    return inp


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

    def __init__(self, memory):
        self.memory = memory
        self.position = 0
        self.max_cycles = 1000000
        self.stop = False
        self.input = None
        self.outputs = list()

    def set_input(self, input_to_set):
        self.input = input_to_set

    def read_and_skip(self):
        value = self.memory[self.position]
        self.position += 1
        return value

    def execute(self):
        num_cycles = 0
        while num_cycles <= self.max_cycles and not self.stop:
            self.process_instruction()
            num_cycles += 1
        if num_cycles >= self.max_cycles:
            raise RecursionError("Reached max cycles.")

    def process_instruction(self):
        code_raw = self.read_and_skip()
        code = Code(code_raw)
        if code.op_code == 1:
            self.process_sum(code)
        elif code.op_code == 2:
            self.process_mul(code)
        elif code.op_code == 3:
            self.process_save_input(code)
        elif code.op_code == 4:
            self.process_output(code)
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

    def process_save_input(self, code):
        self.memory[self.read_and_skip()] = self.input

    def process_output(self, code):
        value = self.read_n_parameter_values(code, 1)[0]
        print(value)
        self.outputs.append(value)

    def process_aritm(self, code, f: callable):
        params = self.read_n_parameter_values(code, 2)
        output_address = self.read_and_skip()
        self.memory[output_address] = f(*params)

    def process_sum(self, code):
        self.process_aritm(code, operator.add)

    def process_mul(self, code):
        self.process_aritm(code, operator.mul)

    def read_n_parameter_values(self, code: Code, number_of_parameter_values_to_get: int):
        values = []
        for n in range(number_of_parameter_values_to_get):
            mode_n = code.get_n_mode(n)
            if mode_n is Modes.POSITION:
                values.append(self.memory[self.read_and_skip()])
            else:
                values.append(self.read_and_skip())
        return values

    def process_jump_if_true(self, code):
        first, second = self.read_n_parameter_values(code, 2)
        if first != 0:
            self.position = second

    def process_jump_if_false(self, code):
        first, second = self.read_n_parameter_values(code, 2)
        if first == 0:
            self.position = second

    def process_less_than(self, code):
        self.process_aritm(code, lambda a, b: int(operator.lt(a, b)))

    def process_equal(self, code):
        self.process_aritm(code, lambda a, b: int(operator.eq(a, b)))


if __name__ == "__main__":
    main("input")
