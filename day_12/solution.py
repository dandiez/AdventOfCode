import itertools
from typing import List
from unittest import TestCase

import numpy as np
from parse import parse

Vector3D = np.ndarray


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [tuple(parse("<x={}, y={}, z={}>", line)) for line in lines]
    inp = [tuple(int(n) for n in str_tuple) for str_tuple in inp]
    return inp


class Body:
    def __init__(
        self, initial_position: Vector3D, initial_velocity: Vector3D, name: str
    ):
        self.pos = initial_position
        self.vel = initial_velocity
        self.name = name

    def __repr__(self):
        return (
            f"{self.name:>10}: pos=<x={self.pos[0]:>3}, y={self.pos[1]:>3}, z={self.pos[2]:>3}>, "
            f"vel=<x={self.vel[0]:>3}, y={self.vel[1]:>3}, z={self.vel[2]:>3}>"
        )

    @property
    def potential_energy(self):
        return sum(abs(self.pos))

    @property
    def kinetic_energy(self):
        return sum(abs(self.vel))

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


class System:
    def __init__(self, bodies: List[Body]):
        self.bodies = bodies
        self.age = 0

    def __repr__(self):
        _repr = ""
        for body in self.bodies:
            _repr += f"{repr(body)}\n"
        return _repr

    def simulate(self, number_of_steps):
        target_age = self.age + number_of_steps
        for self.age in range(self.age, target_age + 1):
            print(f"Energy after {self.age} steps: {self.get_total_energy()}")
            print(self)
            if self.age < target_age:
                self.update_system()

    def get_total_energy(self):
        return sum(body.total_energy for body in self.bodies)

    def update_system(self):
        self.apply_gravity()
        self.apply_velocity()

    def apply_gravity(self):
        for body_a, body_b in itertools.combinations(self.bodies, 2):
            for dimension in range(3):
                if body_a.pos[dimension] > body_b.pos[dimension]:
                    body_a.vel[dimension] -= 1
                    body_b.vel[dimension] += 1
                elif body_a.pos[dimension] < body_b.pos[dimension]:
                    body_a.vel[dimension] += 1
                    body_b.vel[dimension] -= 1

    def apply_velocity(self):
        for body in self.bodies:
            body.pos += body.vel


def part_1(inp, number_of_steps=1000):
    moon_names = ("Io", "Europa", "Ganymede", "Callisto")
    the_system = System(
        [
            Body(np.array(loc), np.array((0, 0, 0)), name)
            for (loc, name) in zip(inp, moon_names)
        ]
    )
    the_system.simulate(number_of_steps)
    return the_system.get_total_energy()


def part_2(inp):
    pass


def test_sample_1(self):
    inp = read_input("sample_1")
    self.assertEqual(179, part_1(inp, number_of_steps=10))


def test_sample_2(self):
    inp = read_input("sample_2")
    self.assertEqual(1940, part_1(inp, number_of_steps=100))


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


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
