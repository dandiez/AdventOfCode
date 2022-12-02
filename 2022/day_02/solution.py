import dataclasses
from enum import Enum, auto
from functools import lru_cache
from unittest import TestCase


class Choice(Enum):
    rock = 1
    paper = 2
    scissors = 3

    @property
    def points(self):
        return self.value


class Outcome(Enum):
    p1_wins = auto()
    p2_wins = auto()
    draw = auto()


@dataclasses.dataclass
class RPSGame:
    p1_score: int = 0
    p2_score: int = 0

    P1_WINNING_HANDS = [
        (Choice.paper, Choice.rock),
        (Choice.scissors, Choice.paper),
        (Choice.rock, Choice.scissors),
    ]

    def play_round(self, p1: Choice, p2: Choice):
        outcome = self.get_outcome(p1, p2)
        self.update_scoring(outcome, p1, p2)

    def update_scoring(self, outcome, p1, p2):
        if outcome is Outcome.draw:
            self.p1_score += 3
            self.p2_score += 3
        elif outcome is Outcome.p1_wins:
            self.p1_score += 6
        elif outcome is Outcome.p2_wins:
            self.p2_score += 6
        self.p1_score += p1.points
        self.p2_score += p2.points

    @classmethod
    def get_outcome(cls, p1: Choice, p2: Choice) -> Outcome:
        if p1 == p2:
            return Outcome.draw
        if (p1, p2) in cls.P1_WINNING_HANDS:
            return Outcome.p1_wins
        return Outcome.p2_wins


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    values = [line.split() for line in lines]
    return values


def part_1(inp):
    CHOICE_FROM_STRING = {
        "A": Choice.rock,
        "X": Choice.rock,
        "B": Choice.paper,
        "Y": Choice.paper,
        "C": Choice.scissors,
        "Z": Choice.scissors,
    }
    inp = [[CHOICE_FROM_STRING[v.strip()] for v in val] for val in inp]  # parse here...
    return play_game_and_get_p2_score(inp)


def play_game_and_get_p2_score(hands: list[[Choice, Choice]]):
    g = RPSGame()
    for hand in hands:
        g.play_round(*hand)
    return g.p2_score


@lru_cache()
def get_p2_choice_for_outcome(desired_outcome: Outcome, p1: Choice):
    for p2 in Choice:
        outcome = RPSGame.get_outcome(p1, p2)
        if outcome == desired_outcome:
            return p2
    raise ValueError()


def part_2(inp):
    FROM_STRING = {
        "A": Choice.rock,
        "X": Outcome.p1_wins,
        "B": Choice.paper,
        "Y": Outcome.draw,
        "C": Choice.scissors,
        "Z": Outcome.p2_wins,
    }
    inp = [[FROM_STRING[v.strip()] for v in val] for val in inp]  # parse here...
    inp = [[p1, get_p2_choice_for_outcome(outcome, p1)] for p1, outcome in inp]
    return play_game_and_get_p2_score(inp)


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
    self.assertEqual(part_1(inp), 15)


def test_sample_2(self):
    inp = read_input("sample_1")
    self.assertEqual(part_2(inp), 12)


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
