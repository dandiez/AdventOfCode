from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    lines = [line.split(" ") for line in lines]  # parse here...
    return lines


def get_x(inp):
    x = 1
    yield x
    for line in inp:
        if line[0] == "noop":
            yield x
        elif line[0] == "addx":
            yield x
            x += int(line[1])
            yield x
    yield x


def part_1(inp):
    signal_strength = 0
    key_cycles = [n + 19 for n in range(300) if not n % 40]
    for n, x in enumerate(get_x(inp)):
        if n in key_cycles:
            N = n + 1
            sigstr = x * N
            signal_strength += sigstr
    return signal_strength


def part_2(inp):
    screen = [[None for n in range(40)] for k in range(6)]
    current_line = 0
    current_column = 0
    for n, x in enumerate(get_x(inp)):
        if n == 240:
            break
        if current_column == 40:
            current_line += 1
            current_column = 0
        if current_column in [x - 1, x, x + 1]:
            screen[current_line][current_column] = "#"
        else:
            screen[current_line][current_column] = "."
        current_column += 1
    for line in screen:
        print("".join(line))


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
    self.assertEqual(13140, part_1(inp))
    part_2(inp)


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
