from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    coords = []
    instructions = []
    for line in lines:
        if "," in line:
            x, y = line.split(",")
            coords.append((int(x), int(y)))
        else:
            eq = line.split("fold along ")[1]
            axis, n = eq.split("=")
            if axis == "x":
                instructions.append((0, int(n)))
            else:
                instructions.append((1, int(n)))
    return set(coords), instructions


def part_1(inp):
    coords, instructions = inp
    operation = instructions[0]
    return len(folded(coords, operation))


def folded(coords, operation):
    axis, location = operation
    new_coords = set()
    for point in coords:
        new_point = list(point)
        delta = new_point[axis] - location
        if delta > 0:
            new_point[axis] -= 2 * delta
        new_coords.add(tuple(new_point))
    return new_coords


def show_grid(coords):
    max_x = max(x for x, y in coords)
    max_y = max(y for x, y in coords)
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in coords:
                line += "#"
            else:
                line += "."
        print(line)


def part_2(inp):
    coords, instructions = inp
    for operation in instructions:
        coords = folded(coords, operation)
    show_grid(coords)



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
    self.assertEqual(17, part_1(inp))
    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
