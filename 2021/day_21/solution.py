from collections import defaultdict
from functools import lru_cache
from itertools import cycle
from unittest import TestCase


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(line[-1]) for line in lines]  # parse here...
    return inp


def cyclic_d100():
    for n in cycle(range(1, 101)):
        yield n


class PracticeGame:
    def __init__(self, p1_start, p2_start):
        self.player_pos = [p1_start, p2_start]
        self.player_points = [0, 0]
        self.roll_count = 0
        self.die = cyclic_d100()
        self.num_players = len(self.player_points)

    def roll(self):
        self.roll_count += 1
        return next(self.die)

    def roll_n(self, n):
        roll_sum = 0
        for _ in range(n):
            roll_sum += self.roll()
        return roll_sum

    def play(self):
        last_score = 0
        for p in cycle(range(self.num_players)):
            if last_score >= 1000:
                return self.player_points[p] * self.roll_count
            roll = self.roll_n(3)
            self.player_pos[p] = self.new_pos(self.player_pos[p], roll)
            self.player_points[p] += self.player_pos[p]
            last_score = self.player_points[p]

    def new_pos(self, old_pos, roll):
        new = old_pos + roll
        return (new - 1) % 10 + 1


def dirac_3d3_one_by_one():
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                yield i + j + k


@lru_cache(None)
def dirac_3d3_all():
    roll_outcomes = defaultdict(int)
    for roll_outcome in dirac_3d3_one_by_one():
        roll_outcomes[roll_outcome] += 1
    return roll_outcomes


@lru_cache(None)
def get_new_state(game_state, roll, win_target=21):
    pos_1, pos_2, points_1, points_2, player_turn, is_won = game_state
    if player_turn == True:
        pos_1 = (pos_1 + roll - 1) % 10 + 1
        points_1 += pos_1
        is_won = points_1 >= win_target
    else:
        pos_2 = (pos_2 + roll - 1) % 10 + 1
        points_2 += pos_2
        is_won = points_2 >= win_target
    return pos_1, pos_2, points_1, points_2, not player_turn, is_won


@lru_cache(None)
def get_new_game_states(game_state: tuple):
    new = set()
    for roll_outcome, count in dirac_3d3_all().items():
        new.add((count, get_new_state(game_state, roll_outcome)))
    return new


def pop_fifo(_dict):
    k, v = next(iter(_dict.items()))
    del _dict[k]
    return k, v


class DiracGame:
    def __init__(self, pos_1, pos_2):
        self.live_games = defaultdict(int)
        self.live_games[(pos_1, pos_2, 0, 0, True, False)] += 1
        self.win_count = defaultdict(int)

    def play(self):
        while sum(self.live_games.values()):
            game, count = pop_fifo(self.live_games)
            new_games = get_new_game_states(game)
            for number_of, game in new_games:
                pos_1, pos_2, points_1, points_2, player_turn, is_won = game
                if is_won:
                    self.win_count[player_turn] += count * number_of
                else:
                    self.live_games[game] += count * number_of
        return max(self.win_count.values())


def part_1(inp):
    game = PracticeGame(*inp)
    return game.play()


def part_2(inp):
    game = DiracGame(*inp)
    return game.play()


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
    self.assertEqual(739785, part_1(inp))
    self.assertEqual(444356092776315, part_2(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
