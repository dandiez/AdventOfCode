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
    inp = [int(val) for val in lines[0]]
    return inp


def part_1(inp):
    layered_image = get_layered_image(inp)
    return get_mult_from_layer_with_least_number_of_zeroes(layered_image)


def get_layered_image(inp):
    width = 25
    height = 6
    image_raw = inp
    flat_image = np.array(image_raw)
    num_layers = len(flat_image) // width // height
    layered_image = np.reshape(flat_image, (num_layers, height, width))
    return layered_image


def get_mult_from_layer_with_least_number_of_zeroes(layered_image):
    min_num_zeroes = np.inf
    layer_mult = None
    for n, layer in enumerate(layered_image):
        unique, counts = np.unique(layer, return_counts=True)
        layer_digits = dict(zip(unique, counts))
        if layer_digits[0] < min_num_zeroes:
            min_num_zeroes = layer_digits[0]
            layer_mult = layer_digits[1] * layer_digits[2]
    return layer_mult


def part_2(inp):
    layered_image = get_layered_image(inp)
    top_layer = layered_image[0]
    for layer in layered_image:
        top_layer = flatten_layers(top_layer, layer)
    render_layer(top_layer)
    return top_layer


def flatten_layers(top, bottom):
    result = top
    for x in range(top.shape[0]):
        for y in range(top.shape[1]):
            result[x][y] = flatten_pixel(top[x][y], bottom[x][y])
    return result


def render_layer(layer):
    chars = {0: '░', 1: '█'}
    for row in layer:
        for num in row:
            print(chars[num], end='')
        print('')


def flatten_pixel(top: int, bottom: int):
    if top == 2:
        return bottom
    return top


if __name__ == "__main__":
    print('*** solving main ***')
    main("input")
