from unittest import TestCase
from parse import parse

def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    xmin, xmax, ymin, ymax = parse('target area: x={:d}..{:d}, y={:d}..{:d}', lines[0])
    return xmin, xmax, ymin, ymax

def part_1(inp):
    xmin, xmax, ymin, ymax = inp
    return sum(-(ymin+1)-n for n in range(-ymin))
    x_good_simulations = {}
    for vx in range(xmax+1):
        target_hits, stopped_at_target = simulate_x(vx, xmin, xmax)
        if target_hits:
            x_good_simulations[vx] = (target_hits, stopped_at_target)
    print(x_good_simulations)



def simulate_x(vx, xmin, xmax):
    target_hits = set()
    step = 0
    x = 0
    while True:
        step += 1
        x += vx
        vx -= 1
        if xmin <= x <= xmax:
            target_hits.add(step)
            if vx == 0:
                return target_hits, True
        if vx <= 0:
            return target_hits, False

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
    self.assertEqual(45, part_1(inp))

def test_sample_2(self):
    pass

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
