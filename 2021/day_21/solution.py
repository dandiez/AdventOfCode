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


practice_die = cyclic_d100()


def cyclic_3d100():
    return sum(next(practice_die) for _ in range(3))


class PracticeGame:
    def __init__(self, pos_1, pos_2):
        self.live_games = defaultdict(int)
        self.live_games[(pos_1, pos_2, 0, 0, True, False)] += 1
        self.win_count = defaultdict(int)
        self.roll_count = 0

    def play(self):
        game = list(self.live_games.keys())[0]
        pos_1, pos_2, points_1, points_2, player_turn, is_won = game
        while not is_won:
            # print(self.live_games, self.win_count)
            game, count = self.live_games.popitem()
            new_games = get_new_game_states(game, practice=True)
            self.roll_count += 3
            for game in new_games:
                pos_1, pos_2, points_1, points_2, player_turn, is_won = game
                if is_won:
                    self.win_count[player_turn] += count
                else:
                    self.live_games[game] += count
        return min(points_1, points_2) * self.roll_count


@lru_cache(None)
def play_turn(game_state, roll, win_target=21):
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


def roll_outcomes():
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                yield i + j + k


@lru_cache(None)
def get_new_game_states(game_state: tuple, practice=False):
    if practice:
        return (play_turn(game_state, cyclic_3d100(), win_target=1000),)
    else:
        new = []
        for roll_outcome in roll_outcomes():
            new.append(play_turn(game_state, roll_outcome))
        return tuple(new)


class DiracGame:
    def __init__(self, pos_1, pos_2):
        self.live_games = defaultdict(int)
        self.live_games[(pos_1, pos_2, 0, 0, True, False)] += 1
        self.win_count = defaultdict(int)

    def play(self):
        while sum(self.live_games.values()):
            # print(self.live_games, self.win_count)
            game, count = self.live_games.popitem()
            new_games = get_new_game_states(game)
            for game in new_games:
                pos_1, pos_2, points_1, points_2, player_turn, is_won = game
                if is_won:
                    self.win_count[player_turn] += count
                else:
                    self.live_games[game] += count
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


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print("*** solving main ***")
    main("input")
