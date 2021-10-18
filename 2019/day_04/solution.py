from typing import Tuple
from unittest import TestCase


def main(input_file):
    """Solve puzzle."""
    # part 1
    inp = read_input(input_file)
    p1 = solve_part(inp)
    print(f"Solution to part 1: {p1}")

    # part 2
    inp = read_input(input_file)
    p2 = solve_part(inp, is_part_1=False)
    print(f"Solution to part 2: {p2}")


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(v) for v in lines[0].split("-")]  # parse here...
    return inp


def solve_part(inp, is_part_1=True):
    min_num, max_num = inp
    min_digits = split_digits(min_num)
    max_digits = split_digits(max_num)
    p1 = count_valid(min_digits, max_digits, is_part_1=is_part_1)
    return p1


def split_digits(num: int) -> Tuple[int]:
    str_int = str(num)
    nums = tuple(int(n) for n in str_int)
    return nums


def count_valid(min_digits, max_digits, is_part_1=True):
    count = 0
    for n0 in range(min_digits[0], max_digits[0] + 1):
        for n1 in range(n0, 10):
            for n2 in range(n1, 10):
                for n3 in range(n2, 10):
                    for n4 in range(n3, 10):
                        for n5 in range(n4, 10):
                            if (n0, n1, n2, n3, n4, n5) >= max_digits:
                                return count
                            if (n0, n1, n2, n3, n4, n5) < min_digits:
                                continue
                            if is_part_1:
                                if has_repeating_part_1(n0, n1, n2, n3, n4, n5):
                                    count += 1
                            else:
                                if has_repeating_part_2(n0, n1, n2, n3, n4, n5):
                                    count += 1


def has_repeating_part_1(*numbers):
    for pos in range(len(numbers) - 1):
        if numbers[pos] == numbers[pos + 1]:
            return True
    return False


def has_repeating_part_2(*numbers):
    numbers = (None,) + numbers + (None,)
    for pos in range(1, len(numbers) - 2):
        same_as_previous = numbers[pos] == numbers[pos - 1]
        same_as_next = numbers[pos] == numbers[pos + 1]
        same_as_next_to_next = numbers[pos] == numbers[pos + 2]
        if not same_as_previous and same_as_next and not same_as_next_to_next:
            return True
    return False


if __name__ == "__main__":
    test_case = TestCase()
    test_case.assertTrue(has_repeating_part_2(1, 1, 2, 3, 4, 5))
    test_case.assertTrue(has_repeating_part_2(1, 1, 1, 1, 2, 2))
    test_case.assertTrue(has_repeating_part_2(1, 1, 2, 2, 3, 3))
    test_case.assertTrue(has_repeating_part_2(1, 1, 2, 2, 2, 5))
    test_case.assertTrue(has_repeating_part_2(6, 1, 2, 3, 5, 5))
    test_case.assertFalse(has_repeating_part_2(1, 1, 1, 3, 4, 5))
    test_case.assertFalse(has_repeating_part_2(1, 2, 3, 4, 4, 4))
    main("input")
