import dataclasses
from unittest import TestCase

BINARY_ADDENDS = tuple(2 ** n for n in reversed(range(9)))


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    filter = {n for n, char in enumerate(lines[0]) if char == "#"}
    image = lines[1:]
    return filter, image


def part_1(inp):
    return enhance_n_times(inp, 2)


def enhance_n_times(inp, n):
    filter, image_raw = inp
    image = BWImage.from_raw(image_raw)
    for n in range(n):
        image.enhance(filter)
    return len(image.pixels)


@dataclasses.dataclass
class BWImage:
    pixels: set
    background: bool = False
    min_r: int = 9e99
    max_r: int = -9e99
    min_c: int = 9e99
    max_c: int = -9e99

    def __post_init__(self):
        self.min_r, self.max_r, self.min_c, self.max_c = self.get_bounds(self.pixels)

    @staticmethod
    def get_bounds(pixels):
        min_r, max_r, min_c, max_c = 9e99, -9e99, 9e99, -9e99
        for r, c in pixels:
            min_r = min(min_r, r)
            max_r = max(max_r, r)
            min_c = min(min_c, c)
            max_c = max(max_c, c)
        return min_r, max_r, min_c, max_c

    @classmethod
    def from_raw(cls, raw_data):
        pixels = set()
        for r, line in enumerate(raw_data):
            for c, char in enumerate(line):
                if char == "#":
                    pixels.add((r, c))
        return cls(pixels=pixels, background=False)

    def render(self):
        pad = 0
        for r in range(self.min_r - pad, self.max_r + 1 + pad):
            line = ""
            for c in range(self.min_c - pad, self.max_c + 1 + pad):
                line += ".#"[(r, c) in self.pixels]
            print(line)

    def enhance(self, filter: set):
        pad = 10
        self.add_padding(pad)
        self.apply_filter(filter)
        self.crop_edges()
        self.enhance_background(filter)
        self.simplify_bounds()

    def apply_filter(self, filter):
        enhanced = set()
        for r, c in self.scan_image(pad=-3):
            if new_pixel_at_loc((r, c), self.pixels, filter):
                enhanced.add((r, c))
        self.pixels = enhanced
        return enhanced

    def enhance_background(self, filter):
        if self.background:
            bin_number = 255
        else:
            bin_number = 0
        self.background = bin_number in filter

    def add_padding(self, pad):
        if self.background:
            for pixel in self.scan_image(pad):
                if not self.within_bounds(pixel):
                    self.pixels.add(pixel)
        self.min_r -= pad
        self.min_c -= pad
        self.max_r += pad
        self.max_c += pad

    def scan_image(self, pad=0):
        for r in range(self.min_r - pad, self.max_r + 1 + pad):
            for c in range(self.min_c - pad, self.max_c + 1 + pad):
                yield r, c

    def within_bounds(self, pixel):
        r, c = pixel
        r_in = self.min_r <= r <= self.max_r
        c_in = self.min_c <= c <= self.max_c
        return r_in and c_in

    def crop_edges(self, quantity=3):
        self.min_r += quantity
        self.min_c += quantity
        self.max_r -= quantity
        self.max_c -= quantity
        self.discard_orphan_pixels()

    def discard_orphan_pixels(self):
        to_discard = set()
        for pixel in self.pixels:
            if not self.within_bounds(pixel):
                to_discard.add(pixel)
        self.pixels.difference_update(to_discard)

    def simplify_bounds(self):
        while self.column_is_background(self.min_c):
            self.min_c += 1
        while self.column_is_background(self.max_c):
            self.max_c -= 1
        while self.row_is_background(self.min_r):
            self.min_r += 1
        while self.row_is_background(self.max_r):
            self.max_r -= 1
        self.discard_orphan_pixels()

    def column_is_background(self, c):
        for r in range(self.min_r, self.max_r + 1):
            if not self.pixel_is_background((r, c)):
                return False
        return True

    def row_is_background(self, r):
        for c in range(self.min_c, self.max_c + 1):
            if not self.pixel_is_background((r, c)):
                return False
        return True

    def pixel_is_background(self, pixel):
        return (pixel in self.pixels) == self.background


def new_pixel_at_loc(loc, image: set, filter: set):
    bin_number = sum(
        addend
        for addend, neighbour in zip(BINARY_ADDENDS, neighbours(*loc))
        if neighbour in image
    )
    return bin_number in filter


def neighbours(r0, c0):
    for r in range(r0 - 1, r0 + 2):
        for c in range(c0 - 1, c0 + 2):
            yield r, c


def part_2(inp):
    return enhance_n_times(inp, 50)


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
    self.assertEqual(35, part_1(inp))


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    # test_sample_1(TestCase())
    # test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
