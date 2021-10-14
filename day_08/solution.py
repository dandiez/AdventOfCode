from unittest import TestCase

import numpy as np


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


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[int(val) for val in line] for line in lines]  # parse here...
    return inp


def part_1(inp):
    width = 25
    height = 6
    images = inp
    for image_raw in images:
        flat_image = np.array(image_raw)
        num_layers = len(flat_image) // width // height
        layered_image = np.reshape(flat_image, (num_layers, height, width))
        return get_mult_from_layer_with_least_number_of_zeroes(layered_image)


def get_mult_from_layer_with_least_number_of_zeroes(layered_image):
    min_num_zeroes = np.inf
    layer_mult = None
    for n, layer in enumerate(np.rollaxis(layered_image, 0)):
        unique, counts = np.unique(layer, return_counts=True)
        layer_digits = dict(zip(unique, counts))
        if layer_digits[0] < min_num_zeroes:
            min_num_zeroes = layer_digits[0]
            layer_mult = layer_digits[1] * layer_digits[2]
    return layer_mult


def part_2(inp):
    pass


def test_sample_1(self):
    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
