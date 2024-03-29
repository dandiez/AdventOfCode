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


def magnitude(snail):
    a, b = snail
    mag = 0
    if isinstance(a, list):
        mag += 3 * magnitude(a)
    else:
        mag += 3 * a
    if isinstance(b, list):
        mag += 2 * magnitude(b)
    else:
        mag += 2 * b
    return mag


def reduce(snail):
    while level(snail) >= 4:
        snail = explode(snail)
    copycat = snail[:]
    snail = split_snail(snail)
    if snail == copycat:
        return snail
    else:
        return reduce(snail)


def level(snail):
    flat = list_as_flat(snail)
    max_level = max(level for level, value in flat)
    return max_level


def flat_as_list(flat):
    while (max_level := max(level for level, value in flat)) > -1:
        for n, (level, value) in enumerate(flat):
            if level == max_level:
                break
        a, b = flat[n], flat[n + 1]
        if a[0] == b[0]:
            flat[n] = [a[0] - 1, [a[1], b[1]]]
            del flat[n + 1]
    return flat[0][1]


def list_as_flat(snail_list, level=0):
    """Flat is a list that stores the [level, value] for all snail values."""
    a, b = snail_list
    if isinstance(a, list):
        flat = list_as_flat(a, level=level + 1)
    else:
        flat = [[level, a]]
    if isinstance(b, list):
        flat.extend(list_as_flat(b, level=level + 1))
    else:
        flat.extend([[level, b]])
    return flat


def explode(snail):
    flat = list_as_flat(snail)
    explode_left_index = -1
    explode_right_index = -1
    val_left = None
    val_right = None
    for n, (level, value) in enumerate(flat):
        if level != 4:
            continue
        if level == 4 and explode_left_index == -1:
            explode_left_index = n
            val_left = value
        else:
            explode_right_index = n
            val_right = value
            break
    if val_left is not None:
        if explode_left_index != 0:
            flat[explode_left_index - 1][1] += val_left
        if explode_right_index != len(flat) - 1:
            flat[explode_right_index + 1][1] += val_right
        flat[explode_left_index][0] -= 1
        flat[explode_left_index][1] = 0
        del flat[explode_right_index]
    return flat_as_list(flat)


def split_snail(snail):
    flat = list_as_flat(snail)
    to_split = []
    for n, (level, value) in enumerate(flat):
        if value >= 10:
            to_split.append((n, value))
            break  # just do one split at a time
    while to_split:
        id, value = to_split.pop()
        new_level = flat[id][0] + 1
        flat[id] = [new_level, value // 2]
        flat.insert(id + 1, [new_level, -(-value // 2)])
    return flat_as_list(flat)


def sum_snails(snail_1, snail_2):
    return [snail_1[:], snail_2[:]]


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
    self.assertEqual(
        [[4, 9], [4, 8], [3, 1], [2, 2], [1, 3], [0, 4]],
        list_as_flat([[[[[9, 8], 1], 2], 3], 4]),
    )
    self.assertEqual(
        [[[[[9, 8], 1], 2], 3], 4],
        flat_as_list([[4, 9], [4, 8], [3, 1], [2, 2], [1, 3], [0, 4]]),
    )
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
