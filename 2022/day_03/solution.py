from typing import Iterable
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def part_1(inp):
    backpacks = [split_in_half(backpack) for backpack in inp]
    all_commmon = [find_common_letter(backpack) for backpack in backpacks]
    return sum(get_priority(letter) for letter in all_commmon)


def split_in_half(backpack: str) -> list[str, str]:
    half = len(backpack) // 2
    return [backpack[:half], backpack[half:]]


def find_common_letter(multiple_strings: list[str]) -> str:
    for letter in multiple_strings[0]:
        if letter_is_in_all_strings(letter, multiple_strings[1:]):
            return letter
    raise ValueError("Cannot find letter in common.")


def letter_is_in_all_strings(letter: str, strings: list[str]) -> bool:
    for string in strings:
        if letter not in string:
            return False
    return True


def get_priority(letter: str) -> int:
    if letter == letter.lower():
        return ord(letter) - ord("a") + 1
    return ord(letter) - ord("A") + 27


def part_2(inp):
    groups = list(in_threes(inp))
    all_commmon = [find_common_letter(group) for group in groups]
    return sum(get_priority(letter) for letter in all_commmon)


def in_threes(backpacks: list[str]) -> Iterable[list[str]]:
    grouped = []
    for backpack in backpacks:
        grouped.append(backpack)
        if len(grouped) == 3:
            yield grouped
            grouped = []


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
    inp = read_input("sample_1")
    self.assertEqual(part_2(inp), 70)
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
