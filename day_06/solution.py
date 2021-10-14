from collections import defaultdict
from unittest import TestCase


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


def read_input(filename="input.txt"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [val.split(')') for val in lines]  # parse here...
    return inp


def part_1(inp):
    parent_child = defaultdict(list)
    child_parent = defaultdict(list)
    space_objects = set()
    for parent, child in inp:
        parent_child[parent].append(child)
        child_parent[child].append(parent)
        space_objects.add(parent)
        space_objects.add(child)

    generations = get_generations(parent_child)
    p1 = sum(generations.values())
    return p1


def get_generations(parent_child):
    gen = 0
    parents = ['COM']
    generations = dict()
    while True:
        gen += 1
        children = []
        for parent in parents:
            children.extend(parent_child[parent])
        for child in children:
            generations[child] = gen
        parents = children
        if not parents:
            return generations


def part_2(inp):
    pass


def test_sample_1(self):
    p1, p2 = main('sample_1')
    self.assertEqual(42, p1)


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
