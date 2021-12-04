from unittest import TestCase

import numpy as np


class Board:

    def __init__(self, numbers):
        self.numbers = np.array(numbers)
        self.seen = np.array([[False] * 5] * 5)
        self.has_won = False

    def has_bingo(self):
        if 5 in np.sum(self.seen, axis=0):
            self.has_won = True
            return True
        if 5 in np.sum(self.seen, axis=1):
            self.has_won = True
            return True
        return False

    def sum_of_unmarked(self):
        not_seen = np.invert(self.seen)
        unmarked = np.multiply(self.numbers, not_seen)
        return np.sum(unmarked)


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    bingo_numbers = [int(n) for n in lines[0].split(',')]
    numbs_for_card_boards = [[int(n) for n in line.split()] for line in lines[1:]]
    all_boards = np.array(numbs_for_card_boards)
    all_boards = all_boards.reshape((-1, 5, 5))
    inp = (bingo_numbers, [Board(board) for board in all_boards])
    return inp


class Bingo:

    def __init__(self, numbers, boards):
        self.numbers = numbers
        self.boards = boards
        self.seen_numbers = []
        self.last_number = None

    def play_bingo(self):
        while self.numbers:
            self.play_next_number()
            winning_board = self.board_with_bingo()
            if winning_board is not None:
                return self.score(winning_board)
        print('no solution')

    def play_bad_bingo(self):
        while self.numbers:
            self.play_next_number()
            if len(self.boards) == 1 and self.boards[0].has_bingo():
                return self.score(self.boards[0])
            self.remove_winning_boards()
        print('no solution')

    def remove_winning_boards(self):
        for board in self.boards:
            if board.has_bingo():
                self.boards.remove(board)

    def score(self, board):
        return self.last_number * board.sum_of_unmarked()

    def play_next_number(self):
        self.last_number = self.numbers.pop(0)
        self.seen_numbers.append(self.last_number)
        self.update_boards(self.last_number)

    def update_boards(self, number):
        for board in self.boards:
            self.update_board(board, number)

    @staticmethod
    def update_board(board: Board, number):
        for i in range(5):
            for j in range(5):
                if board.numbers[i][j] == number:
                    board.seen[i][j] = True

    def board_with_bingo(self):
        for board in self.boards:
            if board.has_bingo():
                return board


def part_1(inp):
    bingo = Bingo(inp[0], inp[1])
    return bingo.play_bingo()


def part_2(inp):
    bingo = Bingo(inp[0], inp[1])
    return bingo.play_bad_bingo()


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
    self.assertEqual(4512, part_1(inp))
    self.assertEqual(1924, part_2(inp))
    pass


def test_sample_2(self):
    pass


if __name__ == "__main__":
    print('*** solving tests ***')
    test_sample_1(TestCase())
    test_sample_2(TestCase())
    print('*** solving main ***')
    main("input")
