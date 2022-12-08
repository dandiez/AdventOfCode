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
            if forest[(x, y)] > tallest:
                tallest = forest[(x, y)]
                visible.add((x, y))
        tallest = -1
        for x in reversed(range(h)):
            if forest[(x, y)] > tallest:
                tallest = forest[(x, y)]
                visible.add((x, y))
    for x in range(h):
        tallest = -1
        for y in range(v):
            if forest[(x, y)] > tallest:
                tallest = forest[(x, y)]
                visible.add((x, y))
        tallest = -1
        for y in reversed(range(v)):
            if forest[(x, y)] > tallest:
                tallest = forest[(x, y)]
                visible.add((x, y))
    return len(visible)


def part_2(inp):
    forest = {(x, y): int(inp[y][x]) for x in range(len(inp[0])) for y in range(len(inp))}
    h = len(inp[0])
    v = len(inp)
    max_score = 0
    for x in range(h):
        for y in range(v):
            score = get_score(forest, h, v, (x, y))
            if score > max_score:
                print(f"{(x, y)}")
                max_score = score
    return max_score


def get_score(forest, h, v, pos):
    x0, y0 = pos
    if (x0 == 0) or x0 == h - 1 or y0 == 0 or y0 == v - 1:
        return 0
    score = 1

    count = 0
    y = y0
    for x in range(x0 - 1, -1, -1):
        count += 1
        hight = forest[x, y]
        if hight >= forest[pos]:
            break
    score *= count

    count = 0
    y = y0
    for x in range(x0 + 1, h):
        count += 1
        hight = forest[x, y]
        if hight >= forest[pos]:
            break
    score *= count

    count = 0
    x = x0
    for y in range(y0 - 1, -1, -1):
        count += 1
        hight = forest[x, y]
        if hight >= forest[pos]:
            break
    score *= count

    count = 0
    x = x0
    for y in range(y0 + 1, v):
        count += 1
        hight = forest[x, y]
        if hight >= forest[pos]:
            break
    score *= count
    return score


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
    self.assertEqual(8, get_score(forest, h, v, (2, 3)))
    self.assertEqual(4, get_score(forest, h, v, (2, 1)))
    self.assertEqual(8, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
