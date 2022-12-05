from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        all = f.read()
        chunks = all.split("\n\n")
        inp = [[int(val) for val in chunk.split("\n") if val] for chunk in chunks]
    return inp


def part_1(inp):
    return max([sum(vals) for vals in inp])


def part_2(inp):
    sums = [sum(vals) for vals in inp]
    sums.sort(reverse=True)
    return sum(sums[0:3])


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
    assert part_1(inp) == 24000
    assert part_2(inp) == 45000


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
