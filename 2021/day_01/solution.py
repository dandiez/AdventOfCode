from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines]  # parse here...
    return inp

def part_1(inp):
    c = 0
    for n in range( len(inp)-1):
        if inp[n] < inp [n+1]:
            c += 1
    return c

def part_2(inp):
    windows = []
    for n in range(len(inp)-2):
        windows.append(inp[n] + inp[n+1] + inp[n+2])
    print(windows)
    return part_1(windows)


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
    pass

def test_sample_2(self):
    pass

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
