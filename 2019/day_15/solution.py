from enum import Enum
from typing import Tuple, Iterable
import networkx as nx
import matplotlib.pyplot as plt

from aoc.grids import UnstructuredGrid
from day_09.solution_not_async import IntcodeComputer

Direction = int
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
ALL_DIRECTIONS = (NORTH, SOUTH, WEST, EAST)


def main(input_file):
    """Solve puzzle and connect part 1 with part 2 if needed."""
    # part 1
    inp = read_input(input_file)
    p1, p2 = part_1_and_2(inp)
    print(f"Solution to part 1: {p1}")
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
        # self.path_taken_thus_far = []

    def move_and_get_feedback(self, direction):
        self.computer.input_queue.put(direction)
        self.computer.execute()
        feedback = self.computer.output_queue.get()
        if feedback == 1 or feedback == 2:
            # self.update_directions_thus_far(direction)
            self.position = Map.get_neighbour_cell(self.position, direction)
        return feedback

    def follow_directions(self, directions: Iterable[Direction]):
        for direction in directions:
            self.move_and_get_feedback(direction)


class TileType(Enum):
    FREE = 0
    WALL = 1
    OXYGEN = 2


ascii_mapping = {
    TileType.FREE: ".",
    TileType.WALL: "#",
    TileType.OXYGEN: "*",
}


def distance(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


class Map:
    def __init__(self):
        self.known_tiles = {(0, 0): TileType.FREE}
        self.path_to_non_blocked_known_tile = {(0, 0): []}
        self.graph = nx.Graph()
        self.graph.add_node((0, 0))
        self.grid = UnstructuredGrid(self.known_tiles)

    def show_as_ascii(self):
        ascii_str = self.grid.render_ascii(lambda x: ascii_mapping[x], "?")
        print(ascii_str)

    def plot_it(self, animate_pause=None):
        self.grid.display_as_plot(lambda x: x.value, animate_pause=animate_pause)

    def add_tile(self, tile_coords, tile_type):
        self.known_tiles[tile_coords] = tile_type
        if tile_type is not TileType.WALL:
            self.graph.add_node(tile_coords)
            for other_tile in self.get_neighbouring_tile_coords(tile_coords):
                if other_tile in self.graph.nodes:
                    self.graph.add_edge(other_tile, tile_coords)

    def all_tiles_have_known_neighbours(self):
        for tile_coords in self.known_tiles:
            for neighbour in self.get_neighbouring_tile_coords(tile_coords):
                if neighbour not in self.known_tiles:
                    return False
        return True

    def get_neighbouring_tile_coords(self, center):
        yield from (
            self.get_neighbour_cell(center, direction) for direction in ALL_DIRECTIONS
        )

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

    def get_next_tile_with_unknown_neighbours(self, current_position):
        cells_to_explore = {
            coords: distance(coords, current_position)
            for coords, tile_type in self.known_tiles.items()
            if tile_type is not TileType.WALL
            and self.cell_has_unknown_neighbours(coords)
        }
        if not cells_to_explore:
            return None
        min_distance = min(cells_to_explore.values())
        for cell, _distance in cells_to_explore.items():
            if _distance == min_distance:
                return cell
        return None

    def cell_has_unknown_neighbours(self, cell_coords):
        for neighbour in self.get_neighbouring_tile_coords(cell_coords):
            if neighbour not in self.known_tiles:
                return True
        return False

    def display_graph(self):
        nx.draw(self.graph)
        plt.show()


class ExplorerAI:
    @classmethod
    def map_out_whole_area(cls, _map: Map, droid: RepairDroid):
        while True:  # not _map.all_tiles_have_known_neighbours():
            # _map.show_as_ascii()
            # print(f"Current map {_map.display_graph()}")
            _map.plot_it(0.0001)
            destination = _map.get_next_tile_with_unknown_neighbours(droid.position)
            # print(f"Going to map cell {destination}")
            if destination is None:
                break
            cls.move_drone_to_destination(droid, _map, destination)
            cls.explore_neighbours(droid, _map)
            if len(_map.known_tiles) % 300 == 0:
                _map.show_as_ascii()
        print("Mapped area")
        _map.show_as_ascii()
        _map.plot_it(animate_pause=10)

    @classmethod
    def find_shortest_sequence_of_directions_to_get_to_oxygen(
        cls, _map: Map, droid: RepairDroid
    ) -> Iterable[Direction]:
        oxygen_tile_coords = [
            coord
            for coord, tile_type in _map.known_tiles.items()
            if tile_type is TileType.OXYGEN
        ][0]
        return cls.get_directions_from_cell_to_cell(_map, (0, 0), oxygen_tile_coords)

    @classmethod
    def move_drone_to_destination(
        cls, droid: RepairDroid, _map: Map, destination: Tuple[int, int]
    ):
        # droid.go_back_to_start()
        # droid.follow_directions(_map.path_to_non_blocked_known_tile[destination])
        origin = droid.position
        if origin == destination:
            return
        directions_iter = cls.get_directions_from_cell_to_cell(
            _map, origin, destination
        )
        droid.follow_directions(directions_iter)

    @classmethod
    def get_directions_from_cell_to_cell(cls, _map: Map, from_cell, to_cell):
        path = nx.shortest_path(_map.graph, from_cell, to_cell)
        path.append(None)
        directions_iter = cls.get_directions_through_path(path)
        return directions_iter

    @classmethod
    def get_directions_through_path(cls, path):
        path_iter = iter(path)
        from_cell = next(path_iter)
        while True:
            to_cell = next(path_iter)
            if to_cell is None:
                return
            yield cls.get_direction_to_neighbouring_cell(from_cell, to_cell)
            from_cell = to_cell

    @staticmethod
    def get_direction_to_neighbouring_cell(from_cell, to_cell):
        delta_x = to_cell[0] - from_cell[0]
        delta_y = to_cell[1] - from_cell[1]
        if not delta_x * delta_y == 0:
            raise ValueError("Cells are not next to each other")
        if delta_x == 1:
            return EAST
        if delta_x == -1:
            return WEST
        if delta_y == 1:
            return NORTH
        if delta_y == -1:
            return SOUTH
        raise ValueError("Cells are too far away")

    @staticmethod
    def explore_neighbours(droid: RepairDroid, _map: Map):
        for direction in ALL_DIRECTIONS:
            target_cell = _map.get_neighbour_cell(droid.position, direction)
            feedback = droid.move_and_get_feedback(direction)
            if feedback == 0:
                _map.add_tile(target_cell, TileType.WALL)
                continue
            elif feedback == 1:
                _map.add_tile(target_cell, TileType.FREE)
            elif feedback == 2:
                _map.add_tile(target_cell, TileType.OXYGEN)
            else:
                raise RuntimeError()
            droid.move_and_get_feedback(opposite(direction))


def part_1_and_2(inp):
    _map = Map()
    droid = RepairDroid(inp)
    ExplorerAI.map_out_whole_area(_map, droid)
    shortest_path = ExplorerAI.find_shortest_sequence_of_directions_to_get_to_oxygen(
        _map, droid
    )
    p1 = len(list(shortest_path))
    shortest_path_to_any = nx.single_source_shortest_path_length(_map.graph, (12, -12))
    p2 = max(shortest_path_to_any.values())
    return p1, p2


if __name__ == "__main__":
    print("*** solving main ***")
    main("input")
