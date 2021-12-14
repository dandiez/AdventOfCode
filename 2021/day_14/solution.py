from collections import defaultdict
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    template = lines[0]
    rules = []
    for line in lines[1:]:
        a, b = line.split(" -> ")
        a0, a1 = a
        rules.append((a, (a0 + b, b + a1)))
    return template, rules


def part_1(inp):
    return solve_polymer(inp, 10)


def part_2(inp):
    return solve_polymer(inp, 40)


def solve_polymer(inp, num_steps):
    template, rules = inp
    pairs = defaultdict(int)
    for n in range(len(template) - 1):
        pairs[template[n : n + 2]] += 1
    for _ in range(num_steps):
        pairs = update(pairs, rules)
    return compute_answer(pairs)


def update(pairs, rules):
    new_pairs = pairs.copy()
    for rule_in, rule_out in rules:
        if pairs[rule_in] > 0:
            new_pairs[rule_in] -= pairs[rule_in]
            new_pairs[rule_out[0]] += pairs[rule_in]
            new_pairs[rule_out[1]] += pairs[rule_in]
    return new_pairs


def compute_answer(pairs):
    elem_count = defaultdict(int)
    for k, val in pairs.items():
        elem_count[k[0]] += val
        elem_count[k[1]] += val
    # round up, to account for first and last element in template having one less instance.
    # other elements will appear twice (2*n) times
    count = [(-(-val // 2)) for val in elem_count.values()]
    return max(count) - min(count)


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
    self.assertEqual(1588, part_1(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
