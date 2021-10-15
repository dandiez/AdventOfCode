from math import gcd
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


MAP_CHARS = {'.': 0, '#': 1}


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[MAP_CHARS[val] for val in line] for line in lines]
    return inp


def get_direction(asteroid, station):
    delta_x = asteroid[0] - station[0]
    delta_y = asteroid[1] - station[1]
    gcd_abs = abs(gcd(delta_x, delta_y))
    return delta_x // gcd_abs, delta_y // gcd_abs


def count_visible_from_station(asteroids, station):
    unique_directions = set()
    for asteroid in asteroids:
        if asteroid == station:
            continue
        unique_directions.add(get_direction(asteroid, station))
    return len(unique_directions)


def part_1(inp):
    asteroids = set()
    for y, row in enumerate(inp):
        for x, val in enumerate(row):
            if val == 1:
                asteroids.add((x, y))
    visible = dict()
    for station in asteroids:
        visible[station] = count_visible_from_station(asteroids, station)
    best_station = max(visible, key=visible.get)
    number_detected = max(visible.values())
    print(f'Best is {best_station} with {number_detected} other asteroids detected.')
    return number_detected


def part_2(inp):
    pass


def test_sample_1(self):
    inp = read_input('sample_1')
    self.assertEqual(210, part_1(inp))


def test_sample_2(self):
    inp = read_input('sample_2')
    self.assertEqual(33, part_1(inp))


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_2(TestCase())
    test_sample_1(TestCase())
    print('*** solving main ***')
    main("input")
