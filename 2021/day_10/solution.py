from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[char for char in line] for line in lines]  # parse here...
    return inp


def part_1(inp):
    # return sum(get_parse_error_points(line) for line in inp)
    ...

char_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}

char_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def get_parse_error_points(line):
    stack = []
    for char in line:
        if is_valid_start(char):
            stack.append(char)
        else:
            expected_start = stack.pop()
            if char != char_pairs[expected_start]:
                return (char_points[char], None)
    endings = [char_pairs[char] for char in reversed(stack)]
    return (0, endings)

def is_valid_start(char):
    return char in char_pairs.keys()


def part_2(inp):
    scores = []
    for line in inp:
        points, ending = get_parse_error_points(line)
        if points == 0:
            scores.append(score_ending(ending))
    return get_middle_score(scores)


def get_middle_score(scores):
    scores.sort()
    return scores[len(scores) // 2 ]


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

ending_scores = {
')': 1 ,
']': 2 ,
'}': 3 ,
'>': 4,
}

def score_ending(ending):
    total = 0
    for char in ending:
        total = 5* total
        total += ending_scores[char]
    return total

def test_sample_1(self):
    inp = read_input("sample_1")
    #self.assertEqual(26397, part_1(inp))
    self.assertEqual(288957, score_ending(list('}}]])})]')))
    self.assertEqual(4, get_middle_score([4, 5, 2]))

def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
