from enum import Enum
from typing import List, Tuple

from day_09.solution_not_async import IntcodeComputer

Direction = int


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


def read_input(filename="input"):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    inp = [int(val) for val in lines[0].split(",")]  # parse here...
    return inp


def opposite(direction):
    if direction == 1:
        return 2
    if direction == 2:
        return 1
    if direction == 3:
        return 4
    if direction == 4:
        return 3
    raise ValueError("unknown direction")


class RepairDroid:

    def __init__(self, inp):
        self.position = (0, 0)
        self.computer = IntcodeComputer(inp)
        self.path_taken_thus_far = []

    def move_and_get_feedback(self, direction):
        self.computer.input_queue.put(direction)
        self.computer.execute()
        feedback = self.computer.output_queue.get()
        if feedback == 1 or feedback == 2:
            self.update_directions_thus_far(direction)
            self.position = Map.get_neighbour_cell(self.position, direction)
        return feedback

    def update_directions_thus_far(self, direction):
        if not self.path_taken_thus_far:
            self.path_taken_thus_far.append(direction)
            return
        if self.path_taken_thus_far[-1] == opposite(direction):
            self.path_taken_thus_far.pop()
        else:
            self.path_taken_thus_far.append(direction)

    def go_back_to_start(self):
        while self.path_taken_thus_far:
            last_direction = self.path_taken_thus_far[-1]
            self.move_and_get_feedback(opposite(last_direction))
        assert self.position==(0,0)

    def follow_directions(self, directions: List[Direction]):
        for direction in directions:
            self.move_and_get_feedback(direction)


class TileType(Enum):
    FREE = 0
    WALL = 1
    OXYGEN = 2


class Map:

    def __init__(self):
        self.known_tiles = {(0, 0): TileType.FREE}
        self.path_to_non_blocked_known_tile = {(0, 0): []}

    def all_tiles_have_known_neighbours(self):
        for tile_coords in self.known_tiles:
            for neighbour in self.get_neighbouring_tile_coords(tile_coords):
                if not neighbour in self.known_tiles:
                    return False
        return True

    def get_neighbouring_tile_coords(self, center):
        yield from (self.get_neighbour_cell(center, direction) for direction in range(1, 5))

    @staticmethod
    def get_neighbour_cell(center, direction):
        if direction == 1:
            return (center[0], center[1] + 1)
        if direction == 2:
            return (center[0], center[1] - 1)
        if direction == 3:
            return (center[0] - 1, center[1])
        if direction == 4:
            return (center[0] + 1, center[1])

    def get_next_tile_with_unknown_neighbours(self):
        for tile_coords, tile in self.known_tiles.items():
            if tile is tile.WALL:
                continue
            for neighbour in self.get_neighbouring_tile_coords(tile_coords):
                if not neighbour in self.known_tiles:
                    return tile_coords
        raise RuntimeError('No tiles left with unknown neighbours')


class ExplorerAI:

    @classmethod
    def map_out_whole_area(cls, map: Map, droid: RepairDroid):
        while not map.all_tiles_have_known_neighbours():
            print(f"Current map {map.known_tiles}")
            destination = map.get_next_tile_with_unknown_neighbours()
            # print(f"Going to map cell {destination}")
            cls.move_drone_to_destination(droid, map, destination)
            cls.explore_neighbours(droid, map)
        print("Mapped area")
        print(f"Current map {map.known_tiles}")

    @classmethod
    def find_shortest_path_to_oxygen(cls, map: Map, droid: RepairDroid) -> List[Direction]:
        ...

    @classmethod
    def move_drone_to_destination(cls, droid: RepairDroid, map: Map, destination:Tuple[int, int]):
        droid.go_back_to_start()
        droid.follow_directions(map.path_to_non_blocked_known_tile[destination])

    @staticmethod
    def explore_neighbours(droid:RepairDroid, map:Map):

        for direction in (1, 2, 3, 4):

            target_cell = map.get_neighbour_cell(droid.position, direction)
            feedback = droid.move_and_get_feedback(direction)

            if feedback == 0:
                map.known_tiles[target_cell] = TileType.WALL
                continue
            elif feedback == 1:
                map.known_tiles[target_cell] = TileType.FREE
            elif feedback == 2:
                map.known_tiles[target_cell] = TileType.OXYGEN
            else:
                raise RuntimeError()
            map.path_to_non_blocked_known_tile[target_cell] = droid.path_taken_thus_far[:]
            droid.move_and_get_feedback(opposite(direction))

def part_1(inp):
    map = Map()
    droid = RepairDroid(inp)
    ExplorerAI.map_out_whole_area(map, droid)
    shortest_path = ExplorerAI.find_shortest_path_to_oxygen(map, droid)
    return len(shortest_path)


def part_2(inp):
    pass


if __name__ == "__main__":
    print('*** solving main ***')
    main("input")
