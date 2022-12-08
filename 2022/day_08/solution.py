from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def part_1(inp):
    forest = {(x, y): int(inp[y][x]) for x in range(len(inp[0])) for y in range(len(inp))}
    h = len(inp[0])
    v = len(inp)
    visible = set()
    for y in range(v):
        tallest = -1
        for x in range(h):
            tallest = check_visibility(forest, tallest, visible, x, y)
        tallest = -1
        for x in reversed(range(h)):
            tallest = check_visibility(forest, tallest, visible, x, y)
    for x in range(h):
        tallest = -1
        for y in range(v):
            tallest = check_visibility(forest, tallest, visible, x, y)
        tallest = -1
        for y in reversed(range(v)):
            tallest = check_visibility(forest, tallest, visible, x, y)
    return len(visible)


def check_visibility(forest, tallest, visible, x, y):
    if forest[(x, y)] > tallest:
        tallest = forest[(x, y)]
        visible.add((x, y))
    return tallest


def part_2(inp):
    forest = {(x, y): int(inp[y][x]) for x in range(len(inp[0])) for y in range(len(inp))}
    h = len(inp[0])
    v = len(inp)
    max_score = 0
    for x in range(h):
        for y in range(v):
            score = get_score(forest, (x, y))
            if score > max_score:
                max_score = score
    return max_score


def get_score(forest, pos):
    score = 1
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        count = get_viewing_distance(forest, pos, direction)
        score *= count
    return score


def vsum(tup1: tuple, tup2: tuple):
    return tuple(v1 + v2 for v1, v2 in zip(tup1, tup2))


def get_viewing_distance(forest, pos0: tuple, direction: tuple):
    n = 0
    p = vsum(pos0, direction)
    hmax = forest[pos0]
    while p in forest:
        h = forest[p]
        p = vsum(p, direction)
        n += 1
        if h >= hmax:
            break
    return n


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
    self.assertEqual(21, part_1(inp))


def test_sample_2(self):
    inp = read_input("sample_1")
    forest = {(x, y): int(inp[y][x]) for x in range(len(inp[0])) for y in range(len(inp))}
    h = len(inp[0])
    v = len(inp)
    self.assertEqual(8, get_score(forest, (2, 3)))
    self.assertEqual(4, get_score(forest, (2, 1)))
    self.assertEqual(8, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
