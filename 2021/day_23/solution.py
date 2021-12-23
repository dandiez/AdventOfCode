import copy
import dataclasses
from unittest import TestCase


@dataclasses.dataclass
class Game:
    entrances = [2, 4, 6, 8]
    corridor: list
    rooms: list[list]
    energy: int = 0
    parent_history: str = ""

    def state(self):
        """State that represents a position uniquely with tuples for hashing purposes."""
        corridor = tuple(self.corridor)
        rooms = tuple(tuple(r) for r in self.rooms)
        return corridor, rooms

    def history(self):
        history = str(self.corridor)
        for r in self.rooms:
            history = history + str(r)
        history = history + str(self.energy)
        return history + "\n" + self.parent_history

    def eval(self):
        """Return if we are done and how much energy we have used thus far."""
        self.shorten_rooms()
        for r in self.rooms:
            if r:
                return False, self.energy  # not done
        return True, self.energy

    def shorten_rooms(self):
        """if the bottom most Amphi is in its room, shrink the room."""
        while self.shorten_one_room():
            pass
            # print("Amphi in its place")

    def shorten_one_room(self):
        for n, room in enumerate(self.rooms):
            if not room:
                continue
            if room[-1] == n:
                room.pop()
                return True
        return False

    def possible_moves(self):
        all_avail_to_move_out = self.all_next_available_to_move_out()
        all_that_can_enter_room = self.all_that_can_enter_room()
        yield from self.generate_games_amphi_moving_out(all_avail_to_move_out)
        yield from self.generate_games_amphi_enter_room(all_that_can_enter_room)

    def generate_games_amphi_enter_room(self, all_that_can_enter_room):
        for pos, amphi in all_that_can_enter_room:
            new_game = copy.deepcopy(self)
            new_game.parent_history = self.history()
            new_game.move_into_room(pos)
            yield new_game

    def move_into_room(self, from_pos):
        amphi = self.corridor[from_pos]
        self.corridor[from_pos] = None
        room = self.rooms[amphi]
        room[-1] = amphi
        distance_to_entrance = abs(self.entrance_id(amphi) - from_pos)
        distance_to_back_of_the_room = len(room)
        distance = distance_to_entrance + distance_to_back_of_the_room
        self.energy += self.calc_energy(amphi, distance)

    def generate_games_amphi_moving_out(self, all_avail_to_move_out):
        for next_available in all_avail_to_move_out:
            room_id, pos, amphi = next_available
            for potential_target in self.valid_pos():
                if self.path_is_clear(self.entrance_id(room_id), potential_target):
                    new_game = copy.deepcopy(self)
                    new_game.parent_history = self.history()
                    new_game.move_from_room(room_id, pos, potential_target)
                    yield new_game

    def move_from_room(self, from_room_id, room_pos, target_pos):
        amphi = self.rooms[from_room_id][room_pos]
        self.rooms[from_room_id][room_pos] = None
        distance_to_entrance = room_pos + 1
        distance_from_entrance_to_target = abs(
            target_pos - self.entrance_id(from_room_id)
        )
        distance = distance_to_entrance + distance_from_entrance_to_target
        self.corridor[target_pos] = amphi
        self.energy += self.calc_energy(amphi, distance)

    @staticmethod
    def calc_energy(amphi, distance):
        return (10 ** amphi) * distance

    def valid_pos(self):
        """position not at entrance and not occupied"""
        for pos, occupant in enumerate(self.corridor):
            if pos not in self.entrances and occupant is None:
                yield pos

    def all_next_available_to_move_out(self) -> list[tuple[int, int, int]]:
        avail_in_rooms = []
        for room_id, room in enumerate(self.rooms):
            next_avail = self.next_available_to_move_out(room)
            if next_avail is None:
                # room is empty
                continue
            pos, amphi = next_avail
            avail_in_rooms.append((room_id, pos, amphi))
        return avail_in_rooms

    def next_available_to_move_out(self, room):
        for pos, a in enumerate(room):
            if a is not None:
                return (pos, a)
        return None

    def all_that_can_enter_room(self):
        ready_rooms = self.ready_rooms()
        all_that_can_go_to_their_room = self.all_with_free_path_to_ready_room(
            ready_rooms
        )
        return all_that_can_go_to_their_room

    def ready_rooms(self):
        """Rooms that can accept their amphis."""
        ready = []
        for n, room in enumerate(self.rooms):
            if self.is_ready(room):
                ready.append(n)
        return ready

    @staticmethod
    def is_ready(room):
        for p in room:
            if p is not None:
                return False
        return True

    def all_with_free_path_to_ready_room(self, ready_rooms):
        amphis_that_can_reach_their_room = []
        for pos, amphi in enumerate(self.corridor):
            if amphi is None:
                continue
            if amphi in ready_rooms:  # there is a ready room for this amphi
                if self.can_reach_entrance(pos, amphi):
                    amphis_that_can_reach_their_room.append((pos, amphi))
        return amphis_that_can_reach_their_room

    def can_reach_entrance(self, from_pos, to_room_id):
        entrance_pos = self.entrance_id(to_room_id)
        return self.path_is_clear(from_pos, entrance_pos)

    def path_is_clear(self, from_pos, to_pos):
        if from_pos == to_pos:
            return True
        if from_pos < to_pos:
            for k in range(from_pos + 1, to_pos + 1):
                if self.corridor[k] is not None:
                    return False
        else:
            for k in range(from_pos - 1, to_pos - 1, -1):
                if self.corridor[k] is not None:
                    return False
        return True

    @staticmethod
    def entrance_id(room_id):
        return Game.entrances[room_id]


def find_min_energy(game):
    ever_seen_states = {}
    live_games = {game.state(): game}
    min_energy = 9e999
    best_game = None
    while live_games:
        h, g = live_games.popitem()
        done, energy = g.eval()
        if done:
            min_energy = min(min_energy, energy)
            best_game = g
            continue
        possible_games = list(g.possible_moves())
        for game in possible_games:
            if game.energy >= min_energy:
                # discard game. It will never beat the current solution.
                continue
            state, energy = game.state(), game.energy
            if state in ever_seen_states:
                if ever_seen_states[state] <= energy:
                    # same position with more energy. Discard it.
                    continue
            live_games[state] = game
            ever_seen_states[state] = energy

    print(best_game)
    return min_energy


game_test_1 = Game(corridor=[None] * 11, rooms=[[1, 0], [2, 3], [1, 2], [3, 0]])

game_1 = Game(corridor=[None] * 11, rooms=[[3, 2], [3, 2], [0, 1], [0, 1]])

game_2 = Game(
    corridor=[None] * 11, rooms=[[3, 3, 3, 2], [3, 2, 1, 2], [0, 1, 0, 1], [0, 0, 2, 1]]
)


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    # inp = read_input(input_file)
    p1 = find_min_energy(game_1)
    print(f"Solution to part 1: {p1}")

    # part 2
    # inp = read_input(input_file)
    p2 = find_min_energy(game_2)
    print(f"Solution to part 2: {p2}")
    return p1, p2


def test_sample_1(self):
    # inp = read_input("sample_1")
    inp = game_test_1
    self.assertEqual(12521, find_min_energy(inp))


if __name__ == "__main__":
    print("*** solving tests ***")
    test_sample_1(TestCase())
    print("*** solving main ***")
    main("input")
