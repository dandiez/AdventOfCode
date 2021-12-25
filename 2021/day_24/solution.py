import dataclasses
import itertools
import queue
from collections import deque, defaultdict
from functools import lru_cache
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [line.split() for line in lines]  # parse here...
    return inp


def split_into_subprograms(inp):
    subprograms = []
    program = []
    for c in inp:
        if c[0] == "inp":
            subprograms.append(program)
            program = []
        program.append(c)
    subprograms.append(program)
    return [p for p in subprograms if p]


@dataclasses.dataclass
class ALU:
    program: list
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0
    inp_stream: deque = dataclasses.field(default_factory=deque)
    trace: list = dataclasses.field(default_factory=list)

    def load_monad(self, monad: list):
        self.inp_stream = deque(monad)

    def print_trace(self):
        for c in self.trace:
            print(c)

    def run(self):
        # print("Run start", self.w, self.x, self.y, self.z)
        for instr in self.program:
            command = instr[0]
            a = instr[1]
            if command == "inp":
                # print(self.w, self.x, self.y, self.z, instr)
                setattr(self, a, self.get_value(self.inp_stream.popleft()))
                continue
            b = self.get_value(instr[2])
            aval = self.get_value(a)
            if command == "add":
                setattr(self, a, aval + b)
            elif command == "mul":
                setattr(self, a, aval * b)
            elif command == "div":
                setattr(self, a, int(aval / b))
            elif command == "mod":
                setattr(self, a, self.alu_mod(aval, b))
            elif command == "eql":
                setattr(self, a, int(aval == b))
            else:
                raise RuntimeError(f"unknown command {command}")
            # self.trace.append((instr, (self.w, self.x, self.y, self.z)))
        # print("Run finished!", self.w, self.x, self.y, self.z)

    @staticmethod
    def alu_mod(aval, bval):
        if aval < 0:
            raise ValueError("Cannot use mod with aval <0")
        if bval <= 0:
            raise ValueError("Cannot use mod with bval <=0")
        return aval % bval

    def get_value(self, raw: str):
        try:
            return int(raw)
        except ValueError:
            return getattr(self, raw)

    def reset(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.inp_stream.clear()
        self.trace = []

    def as_function(self, w, x, y, z, val) -> tuple[int, int, int, int]:
        self.reset()
        self.w, self.x, self.y, self.z = w, x, y, z
        self.inp_stream.append(val)
        self.run()
        return self.w, self.x, self.y, self.z


def get_func(alu_func):
    f = lambda w, x, y, z, val: alu_func(w, x, y, z, val)
    return lru_cache(f)


def part_1(inp):
    subp = split_into_subprograms(inp)
    assert len(subp) == 14
    alus = [ALU(program=p) for p in subp]

    functions = [get_func(alu.as_function) for alu in alus]
    cached_functions = [f for f in functions]
    print(functions)
    min_z = 9e99

    # explore_each_function(functions)

    work_backwards(functions)
    return
    m = (1, 1, 1, 1, 1)
    for _monad in itertools.product(range(9, 0, -1), repeat=9):
        monad = m + _monad
        w, x, y, z = (0, 0, 0, 0)
        for i, f in zip(monad, cached_functions):
            w, x, y, z = f(
                0, 0, 0, z, i
            )  # x, y are multiplied by zero, w is always input
        if z == 0:
            print(monad)
            return monad
        else:
            if z < min_z:
                min_z = z
                print(z, monad)


def work_backwards(functions):
    # explore each function to see what returns a zero
    # f[13] to return zero: z=3, i=1, .. z=11, i=9
    #
    required_z = defaultdict(set)
    required_z[0].add(0)
    associated_i = defaultdict(list)
    func = reversed(functions)
    for n, f in enumerate(func):
        for z in range(26**(min(1+n, 5))):
            for i in range(1, 10):
                _, _, _, z1 = f(0, 0, 0, z, i)
                if z1 in required_z[n]:
                    required_z[n + 1].add(z)
                    associated_i[n].append((z, i))
        # print(f"For function {n} we need the following:{required_z[n+1]} with {associated_i[n]}")
    max_i = dict()
    for k, v in associated_i.items():
        if not v:
            print(f"no solutions for {k}")
        max_i[k] = max(i for z, i in v)
    print(max_i)


def explore_each_function(functions):
    # explore each function for patterns
    for n, f in enumerate(functions):
        for z in range(1000):
            for i in range(1, 10):
                _, _, _, z1 = f(0, 0, 0, z, i)
                if n == 0:
                    assert z1 == 2 + i + 26 * z
                elif n == 1:
                    assert z1 == 4 + i + 26 * z
                elif n == 2:
                    assert z1 == 8 + i + 26 * z
                elif n == 3:
                    assert z1 == 7 + i + 26 * z
                elif n == 4:
                    assert z1 == 12 + i + 26 * z
                elif n == 5:
                    assert z1 == (z // 26) * (25 * int((z % 26) - 14 != i) + 1) + (
                        i + 7
                    ) * int((z % 26) - 14 != i)
                elif n == 6:
                    assert z1 == (z // 26) * (25 * int((z % 26) != i) + 1) + (
                        i + 10
                    ) * int((z % 26) != i)
                elif n == 7:
                    assert z1 == 14 + i + 26 * z
                elif n == 8:
                    assert z1 == (z // 26) * (25 * int((z % 26) - 10 != i) + 1) + (
                        i + 2
                    ) * int((z % 26) - 10 != i)
                elif n == 9:
                    assert z1 == 6 + i + 26 * z
                elif n == 10:
                    assert z1 == (z // 26) * (25 * int((z % 26) - 12 != i) + 1) + (
                        i + 8
                    ) * int((z % 26) - 12 != i)
                elif n == 11:
                    assert z1 == (z // 26) * (25 * int((z % 26) - 3 != i) + 1) + (
                        i + 11
                    ) * int((z % 26) - 3 != i)
                elif n == 12:
                    assert z1 == (z // 26) * (25 * int((z % 26) - 11 != i) + 1) + (
                        i + 5
                    ) * int((z % 26) - 11 != i)
                elif n == 13:
                    assert z1 == (z // 26) * (25 * int((z % 26) - 2 != i) + 1) + (
                        i + 11
                    ) * int((z % 26) - 2 != i)
                else:
                    print(n, z, i, f(0, 0, 0, z, i))


def part_1_brute(inp):
    c = ALU(program=inp)
    min_z = 9e99
    for monad in itertools.product(range(9, 0, -1), repeat=14):
        c.reset()
        c.load_monad(monad)
        try:
            c.run()
            # for a in c.trace:
            #    print(a)
        except Exception:
            continue
        if c.z == 0:
            return monad
        else:
            if c.z < min_z:
                min_z = c.z
                print(c.z, monad)


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
    # inp = read_input("sample_1")
    c = ALU(program=[["inp", "x"], ["mul", "x", "-1"]])
    c.inp_stream.append(7)
    c.run()
    self.assertEqual(-7, c.x)

    c = ALU(program=[["inp", "z"], ["inp", "x"], ["mul", "z", "3"], ["eql", "z", "x"]])
    c.load_monad(["3", "9"])
    c.run()
    self.assertEqual(1, c.z)

    c.reset()
    c.load_monad(["3", "10"])
    c.run()
    self.assertEqual(0, c.z)

    c.reset()
    c.load_monad(["3", "8"])
    c.run()
    self.assertEqual(0, c.z)

    c.reset()
    c.load_monad(["-3", "-9"])
    c.run()
    self.assertEqual(1, c.z)

    test_prog = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""
    inp = [line.split() for line in test_prog.split("\n")]
    c = ALU(program=inp)
    c.load_monad(["0"])
    c.run()
    self.assertEqual((0, 0, 0, 0), (c.w, c.x, c.y, c.z))
    c.reset()
    c.load_monad(["1"])
    c.run()
    self.assertEqual((0, 0, 0, 1), (c.w, c.x, c.y, c.z))
    c.reset()
    c.load_monad(["5"])
    c.run()
    self.assertEqual((0, 1, 0, 1), (c.w, c.x, c.y, c.z))
    c.reset()
    c.load_monad(["15"])
    c.run()
    self.assertEqual((1, 1, 1, 1), (c.w, c.x, c.y, c.z))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
