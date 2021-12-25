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
    # A  list comprehension messes up the variables and results in bad lambdas
    # need to have an aux function instead.
    f = lambda w, x, y, z, val: alu_func(w, x, y, z, val)
    return lru_cache(f)


def get_direct_functions():
    functions = []
    functions.append(lambda z, i: 2 + i + 26 * z)
    functions.append(lambda z, i: 4 + i + 26 * z)
    functions.append(lambda z, i: 8 + i + 26 * z)
    functions.append(lambda z, i: 7 + i + 26 * z)
    functions.append(lambda z, i: 12 + i + 26 * z)
    functions.append(
        lambda z, i: (z // 26) * (25 * int((z % 26) - 14 != i) + 1)
        + (i + 7) * int((z % 26) - 14 != i)
    )
    functions.append(
        lambda z, i: (z // 26) * (25 * int((z % 26) != i) + 1)
        + (i + 10) * int((z % 26) != i)
    )
    functions.append(lambda z, i: 14 + i + 26 * z)
    functions.append(
        lambda z, i: (z // 26) * (25 * int((z % 26) - 10 != i) + 1)
        + (i + 2) * int((z % 26) - 10 != i)
    )
    functions.append(lambda z, i: 6 + i + 26 * z)
    functions.append(
        lambda z, i: (z // 26) * (25 * int((z % 26) - 12 != i) + 1)
        + (i + 8) * int((z % 26) - 12 != i)
    )
    functions.append(
        lambda z, i: (z // 26) * (25 * int((z % 26) - 3 != i) + 1)
        + (i + 11) * int((z % 26) - 3 != i)
    )
    functions.append(
        lambda z, i: (z // 26) * (25 * int((z % 26) - 11 != i) + 1)
        + (i + 5) * int((z % 26) - 11 != i)
    )
    functions.append(
        lambda z, i: (z // 26) * (25 * int((z % 26) - 2 != i) + 1)
        + (i + 11) * int((z % 26) - 2 != i)
    )
    return functions


def validate_functions(alu_fs, fs):
    """Validate the simplified functions."""
    # The only value carried across is z (the others are reset by multiplication with zero.
    assert len(alu_fs) == len(fs)
    for af, f in zip(alu_fs, fs):
        for i in range(1, 10):
            for z in range(1, 1000):
                _, _, _, z_af = af(0, 0, 0, z, i)
                z_f = f(z, i)
                assert z_af == z_f


def solve_part(inp, is_part_1=True):
    """Solve the puzzle."""
    # Upon inspection, we see that the input is really 14 copies of nearly the same program
    subp = split_into_subprograms(inp)
    assert len(subp) == 14
    alus = [ALU(program=p) for p in subp]

    # we can cache the function values (still no use in a brute force approach)
    alu_functions = [get_func(alu.as_function) for alu in alus]

    # we can reverse engineer the program to get equivalent functions which we can verify.
    functions = get_direct_functions()
    validate_functions(alu_functions, functions)

    # Each of the 14 functions either increases (*26) the result or decreases it.
    # However, the ones that are supposed to decrease the result may also increase it.
    # Monitor these functions and discard values that don't decrease when they should.
    must_decrease = [
        False,
        False,
        False,
        False,
        False,
        True,
        True,
        False,
        True,
        False,
        True,
        True,
        True,
        True,
    ]
    assert len(must_decrease) == 14

    # working from the end, find what intermediate z results would lead to a valid monad
    leading_to_zero_at_the_end = work_backwards(functions)

    # working from the start, feed the initial z=0 for different i values
    monads = {(-1,): 0}
    for n, func in enumerate(functions):
        print(f"Running function {n}. Num monads is {len(monads)}.")
        expected_decrease = must_decrease[n]
        new_monads = {}
        reverse_lookup = {}
        for i in range(9, 0, -1):
            print(f"Running i={i}")
            for old_monad, z in monads.items():
                monad = old_monad + (i,)
                z1 = func(z, i)
                if expected_decrease:
                    if z1 > z * 26:
                        # not enough divide by 26 operations afterwards
                        continue
                if n + 1 in leading_to_zero_at_the_end:
                    if not z1 in leading_to_zero_at_the_end[n + 1]:
                        # this solution will not lead to a final zero
                        continue
                if z1 in reverse_lookup:
                    old_monad = reverse_lookup[z1]
                    if is_part_1:
                        if monad < old_monad:
                            # do not store z1 for this monad if another better monad has the same z
                            continue
                    else:
                        if monad > old_monad:
                            continue
                new_monads[monad] = z1
                reverse_lookup[z1] = monad
        monads = new_monads
    return "".join(str(v) for v in reverse_lookup[0][1:])


def work_backwards(functions):
    # explore each function to see what returns a zero
    # f[13] to return zero: z=3, i=1, .. z=11, i=9
    #
    required_z = defaultdict(set)
    required_z[14].add(0)
    associated_i = defaultdict(list)
    func = reversed(functions)
    for _n, f in enumerate(func):
        n = 13 - _n
        if n == 8:
            # going backwards more takes forever... break here and we'll meet in the middle
            return required_z
        print(f"working backwards, checking function {n}")
        print(
            f"this function must produce any of the {len(required_z[n+1])} valid outcomes."
        )
        for i in range(1, 10):
            max_z = 26 ** (1 + _n)
            print(f"Checking i={i} up to z={max_z}")
            for z in range(max_z):
                z1 = f(z, i)
                if z1 in required_z[n + 1]:
                    required_z[n].add(z)
        print(
            f"previous function should produce one of {len(required_z[n])} valid outcomes."
        )


def explore_each_function(functions):
    # confirm what each monad digit does
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


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1 = solve_part(inp)

    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = solve_part(inp, is_part_1=False)
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


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
