import dataclasses
import math
from collections import defaultdict
from typing import Dict
from unittest import TestCase
from scipy.optimize import fsolve
import numpy as np


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    inp = read_input(input_file)
    p1, p2 = part_1_and_2(inp)
    print(f"Solution to part 1: {p1}")
    print(f"Solution to part 2: {p2}")
    return p1, p2


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


@dataclasses.dataclass
class ReactionResults:
    desired_output_quantity: int
    actual_outputs: Dict[str, int]
    actual_inputs: Dict[str, int]


class Reaction:
    def __init__(self, reaction_str):
        self.inputs: Dict[str, int] = dict()
        self.outputs: Dict[str, int] = dict()
        self.parse_reaction(reaction_str)
        self.info_output_element()  # validates output list has only one element

    def parse_reaction(self, reaction_str):
        inputs_string, outputs_string = reaction_str.split("=>")
        self.inputs = self._parse_side(inputs_string)
        self.outputs = self._parse_side(outputs_string)

    def _parse_side(self, num_elem_str: str):
        num_elem_inputs = [split_item.strip() for split_item in num_elem_str.split(",")]
        return {
            elem_num.split(" ")[1]: int(elem_num.split(" ")[0])
            for elem_num in num_elem_inputs
        }

    def info_output_element(self) -> str:
        if len(self.outputs) != 1:
            raise NotImplementedError(
                "Can only deal with reactions that produce one output."
            )
        return next(iter(self.outputs))

    def calculate(self, desired_output_quantity: int) -> ReactionResults:
        minimum_output_quantity = next(iter(self.outputs.values()))
        number_of_times = -(-desired_output_quantity // minimum_output_quantity)
        actual_outputs = {
            element: quantity * number_of_times
            for element, quantity in self.outputs.items()
        }
        actual_inputs = {
            element: quantity * number_of_times
            for element, quantity in self.inputs.items()
        }
        results = ReactionResults(
            desired_output_quantity=desired_output_quantity,
            actual_outputs=actual_outputs,
            actual_inputs=actual_inputs,
        )
        # print(f"{self.info_output_element()}: {results}")
        return results

    def __repr__(self):
        return f"<Reaction: {self.inputs} => {self.outputs}>"


def produce_n_fuel(all_reactions, n):
    stock = defaultdict(int)
    stock["FUEL"] -= n
    negative_stock = get_elements_with_demand(stock)
    while negative_stock != {"ORE"}:
        for element in negative_stock:
            if element == "ORE":
                continue
            desired_output_quantity = stock[element]
            reaction = all_reactions[element]
            results = reaction.calculate(-desired_output_quantity)
            for (
                actual_output_element,
                actual_output_quantity,
            ) in results.actual_outputs.items():
                stock[actual_output_element] += actual_output_quantity
            for (
                actual_input_element,
                actual_input_quantity,
            ) in results.actual_inputs.items():
                stock[actual_input_element] -= actual_input_quantity
        negative_stock = get_elements_with_demand(stock)
    return -stock["ORE"]


def part_1_and_2(inp, is_part_1=False):
    all_reactions = dict()
    for line in inp:
        reaction = Reaction(line)
        all_reactions[reaction.info_output_element()] = reaction
    p1 = produce_n_fuel(all_reactions, 1)
    if is_part_1:
        return p1

    # part 2
    target = 1000000000000
    f = lambda x: produce_n_fuel(all_reactions, x) - target
    solution = fsolve(f, np.array([target / p1]))
    n_ceil = math.ceil(solution[0])
    if produce_n_fuel(all_reactions, n_ceil) < target:
        p2 = n_ceil
    else:
        n_floor = math.floor(solution[0])
        p2 = n_floor
    return p1, p2


def get_elements_with_demand(stock):
    return {element for element, quantity in stock.items() if quantity < 0}


def test_samples(self):
    expected = ((13312, 82892753), (180697, 5586022), (2210736, 460664))
    for n in range(2, 5):
        inp = read_input(f"sample_{n}.txt")
        self.assertEqual(expected[n - 2], part_1_and_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_samples(TestCase())
    print("*** solving main ***")
    main("input")
