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

class Simulation:
    def __init__(self, xmin, xmax, ymin, ymax, vx, vy):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.vx = vx
        self.vy = vy
        self.x = 0
        self.y = 0
        self.num_solutions = 0

    def simulate(self):
        while True:
            self.simulate_step()
            if self.in_target():
                self.num_solutions+=1
                break
            if self.impossible_to_reach():
                break

    def simulate_step(self):
        self.x += self.vx
        self.y += self.vy
        if self.vx > 0:
            self.vx -= 1
        self.vy -= 1

    def in_target(self):
        x_in = self.xmin <= self.x <= self.xmax
        y_in = self.ymin <= self.y <= self.ymax
        return x_in and y_in

    def impossible_to_reach(self):
        if self.y < self.ymin:
            return True
        if self.vx <= 0:
            if not (self.xmin <= self.x <= self.xmax):
                return False



def part_2(inp):
    xmin, xmax, ymin, ymax = inp
    num_solutions = 0
    for vx in range(1, xmax+1):
        for vy in range(ymin-1, -ymin+2):
            s = Simulation(xmin, xmax, ymin, ymax, vx, vy)
            s.simulate()
            num_solutions += s.num_solutions
    return num_solutions



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
    self.assertEqual(112, part_2(inp))

def test_sample_2(self):
    pass

if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
