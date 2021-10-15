import dataclasses
from typing import Dict
from unittest import TestCase

from day_09.solution_not_async import IntcodeComputer


def read_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = lines[0].split(",")  # parse here...
    inp = [int(v) for v in inp]
    return inp


@dataclasses.dataclass(eq=True, frozen=True)
class Vector:
    x: int
    y: int


@dataclasses.dataclass(eq=True, frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Vector):
            return Coords(x=self.x + other.x, y=self.y + other.y)


UP = Vector(x=0, y=1)
RIGHT = Vector(x=1, y=0)
DOWN = Vector(x=0, y=-1)
LEFT = Vector(x=-1, y=0)

next_clockwise = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}

next_anti_clockwise = {
    UP: LEFT,
    RIGHT: UP,
    DOWN: RIGHT,
    LEFT: DOWN,
}

GridColorDict = Dict[Coords, int]


class Robot:

    def __init__(self, computer: IntcodeComputer, starting_position: Coords, starting_orientation: Vector):
        self.computer = computer
        self.current_position = starting_position
        self.current_orientation: Vector = starting_orientation
        self.painted_panels: GridColorDict = dict()

    def get_color_and_turn(self, input_color):
        self.computer.input_queue.put(input_color)
        self.computer.execute()
        color, turn = self.computer.get_outputs_as_list()
        return color, turn

    def move_to_new_position(self, turn):
        if turn == 0:
            # turn left 90 degrees (anti clockwise from the top)
            self.current_orientation = next_anti_clockwise[self.current_orientation]
        elif turn == 1:
            self.current_orientation = next_clockwise[self.current_orientation]
        else:
            raise ValueError(f'unexpected turn value {turn}')
        self.current_position += self.current_orientation

    def paint(self, color):
        self.painted_panels[self.current_position] = color

    def get_number_of_panels_painted(self):
        return len(self.painted_panels)

    def get_color_at_current_position(self):
        if not self.current_position in self.painted_panels:
            return 0
        return self.painted_panels[self.current_position]


def part_1(inp):
    comp = IntcodeComputer(inp)
    robot = Robot(comp, Coords(x=0, y=0), UP)
    while not robot.computer.execution_ended():
        color, turn = robot.get_color_and_turn(robot.get_color_at_current_position())
        robot.paint(color)
        robot.move_to_new_position(turn)

    return robot.get_number_of_panels_painted()


def part_2(inp):
    pass


def test_sample_1(self):
    pass


def test_sample_2(self):
    pass


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
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
