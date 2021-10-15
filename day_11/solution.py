import dataclasses
from collections import defaultdict
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

    def __init__(self, computer: IntcodeComputer, starting_position: Coords, starting_orientation: Vector,
                 starting_color):
        self.computer = computer
        self.current_position = starting_position
        self.current_orientation: Vector = starting_orientation
        self.painted_panels: GridColorDict = {self.current_position: starting_color}

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

    def render_painted_panels(self):
        render = ''
        white_panels = defaultdict(int,
                                   ((coord, color) for coord, color in self.painted_panels.items() if color == 1),
                                   )
        min_x = min(coords.x for coords in white_panels.keys())
        max_x = max(coords.x for coords in white_panels.keys())
        min_y = min(coords.y for coords in white_panels.keys())
        max_y = max(coords.y for coords in white_panels.keys())
        padding = 1
        for y in reversed(range(min_y - padding, max_y + 1 + padding)):
            # y is in reversed order because screen_y is -y (prints downwards)
            for x in range(min_x - padding, max_x + 1 + padding):
                if Coords(x=x, y=y) in white_panels:
                    render += "█"
                else:
                    render += '░'
            render += '\n'
        print(render)


def part_n(inp, part_1=True):
    if part_1:
        starting_color = 0
    else:
        starting_color = 1
    comp = IntcodeComputer(inp)
    robot = Robot(comp, Coords(x=0, y=0), UP, starting_color=starting_color)
    while not robot.computer.execution_ended():
        color, turn = robot.get_color_and_turn(robot.get_color_at_current_position())
        robot.paint(color)
        robot.move_to_new_position(turn)
    robot.render_painted_panels()
    return robot.get_number_of_panels_painted()


def part_2(inp):
    return part_n(inp, part_1=False)

def part_1(inp):
    return part_n(inp)

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
    print('*** solving main ***')
    main("input")
