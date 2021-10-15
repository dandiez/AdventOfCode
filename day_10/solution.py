import dataclasses
from collections import defaultdict
from math import gcd, atan2, pi
from unittest import TestCase


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1, p2 = part_1(inp)
    print(f"Solution to part 1: {p1}")

    # part 2
    print(f"Solution to part 2: {p2}")
    return p1, p2


MAP_CHARS = {'.': 0, '#': 1}


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [[MAP_CHARS[val] for val in line] for line in lines]
    return inp


def get_direction(asteroid, station):
    return get_direction_and_distance(asteroid, station)[0]


def get_direction_and_distance(asteroid, station):
    delta_x = asteroid[0] - station[0]
    delta_y = asteroid[1] - station[1]
    gcd_abs = abs(gcd(delta_x, delta_y))
    return (delta_x // gcd_abs, delta_y // gcd_abs), delta_x * delta_x + delta_y * delta_y


def count_visible_from_station(asteroids, station):
    unique_directions = set()
    for asteroid in asteroids:
        if asteroid == station:
            continue
        unique_directions.add(get_direction(asteroid, station))
    return len(unique_directions)


@dataclasses.dataclass
class Asteroid:
    coords: tuple
    direction: tuple
    distance: int


def order_asteroids_on_same_line_by_distance(detailed_asteroids):
    for asteroid_direction, asteroids in detailed_asteroids.items():
        if len(asteroids) > 1:
            # put closest last so we can pop from the list
            asteroids.sort(key=lambda x: x.distance, reverse=True)


def get_angle_to_top(direction):
    dx = direction[0]
    dy = direction[1]
    angle = pi / 4 - atan2(dx, dy)
    return angle


def part_1(inp):
    # part 1
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
    p1 = number_detected

    # part 2
    detailed_asteroids = defaultdict(list)
    for asteroid in asteroids:
        if asteroid == best_station:
            continue
        direction, distance = get_direction_and_distance(asteroid, best_station)
        a = Asteroid(coords=asteroid, direction=direction, distance=distance)
        detailed_asteroids[get_angle_to_top(direction)].append(a)
    order_asteroids_on_same_line_by_distance(detailed_asteroids)
    detailed_asteroids = dict(sorted(detailed_asteroids.items()))
    count = 0
    still_some_left = True
    while still_some_left:
        still_some_left = False
        for k, v in detailed_asteroids.items():
            if not v:
                continue
            count += 1
            asteroid_gone = v.pop()
            # print(f'count {count}: {asteroid_gone}')
            still_some_left = True
            if count == 200:
                p2 = asteroid_gone.coords[0] * 100 + asteroid_gone.coords[1]

    return p1, p2


def part_2(inp):
    pass


def test_sample_1(self):
    inp = read_input('sample_1')
    self.assertEqual((210, 802), part_1(inp))


def test_sample_2(self):
    inp = read_input('sample_2')
    self.assertEqual(33, part_1(inp)[0])


if __name__ == "__main__":
    print('*** solving tests ***')
    # test_sample_2(TestCase())
    test_sample_1(TestCase())
    print('*** solving main ***')
    main("input")
