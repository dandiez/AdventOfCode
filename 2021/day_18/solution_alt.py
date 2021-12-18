import dataclasses
from typing import Optional
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [eval(line) for line in lines]  # parse here...
    return inp


def part_1(inp):
    snail = inp[0]
    for s in inp[1:]:
        snail = sum_snails(snail, s)
        snail = reduce(snail)
    return magnitude(snail)


@dataclasses.dataclass
class SnailNumber:
    parent: Optional["SnailNumber"] = None
    children: Optional[list["SnailNumber", "RegularNumber"]] = None

    def walk_generations(self, gen=0, backwards=False):
        children = reversed(self.children) if backwards else self.children
        for child in children:
            if isinstance(child, RegularNumber):
                yield (gen, child.value)
            else:
                yield from child.walk_generations(gen=gen + 1)


@dataclasses.dataclass
class RegularNumber:
    value: int
    parent: SnailNumber


def snail_number_as_list(snail: [SnailNumber, RegularNumber]):
    if isinstance(snail, RegularNumber):
        return snail.value
    return [snail_number_as_list(child) for child in snail.children]


def get_snail_number(raw_snail: [list, int], parent=None):
    if isinstance(raw_snail, int):
        return RegularNumber(raw_snail, parent=parent)
    if len(raw_snail) != 2:
        raise ValueError("A raw snail must have two children")
    snail = SnailNumber(parent=parent)
    snail.children = [
        get_snail_number(raw_snail[0], parent=snail),
        get_snail_number(raw_snail[1], parent=snail),
    ]
    return snail


def part_2(inp):
    max_mag = 0
    for snail_1 in inp:
        for snail_2 in inp:
            if snail_1 != snail_2:
                mag = magnitude(reduce(sum_snails(snail_1, snail_2)))
                max_mag = max(max_mag, mag)
                if max_mag == mag:
                    print(mag)
    return max_mag


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
    s = get_snail_number(inp[0])
    for raw_snail in inp:
        self.assertEqual(raw_snail, snail_number_as_list(get_snail_number(raw_snail)))
    self.assertEqual(
        [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
        explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]),
    )
    self.assertEqual([[[[0, 9], 2], 3], 4], explode([[[[[9, 8], 1], 2], 3], 4]))
    self.assertEqual(
        [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]),
    )
    self.assertEqual(
        [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
        split_snail([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]),
    )
    self.assertEqual(
        [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]],
        reduce([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]),
    )
    self.assertEqual(143, magnitude([[1, 2], [[3, 4], 5]]))
    self.assertEqual(3993, part_2(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
