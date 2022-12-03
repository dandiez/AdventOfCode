from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def split_in_half(backpack: str) -> tuple[str, str]:
    half = len(backpack) // 2
    return backpack[:half], backpack[half:]


def find_common(pocket_1: str, pocket_2: str) -> str:
    for letter in pocket_1:
        if letter in pocket_2:
            return letter


def get_priority(letter: str) -> int:
    if letter == letter.lower():
        return ord(letter) - ord("a") + 1
    return ord(letter) - ord("A") + 27


def part_1(inp):
    pockets = [split_in_half(backpack) for backpack in inp]
    all_commmon = [find_common(*pockets) for pockets in pockets]
    return sum(get_priority(letter) for letter in all_commmon)


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
    inp = read_input("sample_1")
    self.assertEqual(part_1(inp), 157)


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
