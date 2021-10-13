from typing import Tuple


def main(input_file):
    """Solve puzzle."""
    # part 1
    inp = read_input(input_file)
    p1 = part_1(inp)
    print(f"Solution to part 1: {p1}")


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(v) for v in lines[0].split("-")]  # parse here...
    return inp


def part_1(inp):
    min_num, max_num = inp
    min_digits = split_digits(min_num)
    max_digits = split_digits(max_num)
    p1 = count_valid(min_digits, max_digits)
    return p1


def split_digits(num: int) -> Tuple[int]:
    str_int = str(num)
    nums = tuple(int(n) for n in str_int)
    return nums


def count_valid(min_digits, max_digits):
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
                            if n0 == n1:
                                count += 1
                            elif n1 == n2:
                                count += 1
                            elif n2 == n3:
                                count += 1
                            elif n3 == n4:
                                count += 1
                            elif n4 == n5:
                                count += 1


if __name__ == "__main__":
    main("input")
