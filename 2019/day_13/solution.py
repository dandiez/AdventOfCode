import asyncio
import dataclasses
from asyncio import Queue
from enum import Enum
from typing import Iterable, Tuple, Dict, List

from day_09.solution import IntcodeComputer


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
    inp = [int(val) for val in lines[0].split(',')]  # parse here...
    return inp


class TilesType(Enum):
    EMPTY = 0  # is an empty tile. No game object appears in this tile.
    WALL = 1  # is a wall tile. Walls are indestructible barriers.
    BLOCK = 2  # is a block tile. Blocks can be broken by the ball.
    PADDLE = 3  # is a horizontal paddle tile. The paddle is indestructible.
    BALL = 4  # is a ball tile. The ball moves diagonally and bounces off objects.


class TileProperties:

    def __init__(self, int_type: int):
        self.tile_type = TilesType(int_type)


@dataclasses.dataclass(eq=True)
class Location:
    x: int
    y: int


class Tile:

    def __init__(self, x: int, y: int, int_type: int):
        self.location = Location(x, y)
        self.properties = TileProperties(int_type)


@dataclasses.dataclass
class CoordLimits:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def x_range(self) -> Iterable[int]:
        yield from range(self.x_min, self.x_max + 1)

    def y_range(self) -> Iterable[int]:
        yield from range(self.y_min, self.y_max + 1)


class ScreenData:

    def __init__(self):
        self.tiles = dict()

    def add_tile(self, tile: Tile):
        self.tiles[(tile.location.x, tile.location.y)] = tile

    def get_tiles_as_dict(self) -> Dict[Tuple[int, int], Tile]:
        return self.tiles

    @staticmethod
    def get_min_max_tile_coords(tile_coords: Iterable[Tuple[int, int]]):
        limits = CoordLimits(x_min=9999999, x_max=-9999999, y_min=9999999, y_max=-9999999)
        for x, y in tile_coords:
            limits.x_min = min(limits.x_min, x)
            limits.x_max = max(limits.x_max, x)
            limits.y_min = min(limits.y_min, y)
            limits.y_max = max(limits.y_max, y)
        return limits


class GameState:

    def __init__(self):
        self.screen_data: ScreenData = ScreenData()
        self.score: int = -1


class ScreenASCIIRender:
    tile_chars = {
        TilesType.EMPTY: '░',
        TilesType.BALL: '●',
        TilesType.WALL: '█',
        TilesType.BLOCK: '▓',
        TilesType.PADDLE: '═'
    }
    unknown_char = '?'

    @classmethod
    def render(cls, game_state: GameState):
        render: str = f"score: {game_state.score}\n"
        tiles_as_dict = game_state.screen_data.get_tiles_as_dict()
        limits = game_state.screen_data.get_min_max_tile_coords(tiles_as_dict.keys())
        for y in limits.y_range():
            for x in limits.x_range():
                tile = tiles_as_dict.get((x, y), None)
                char = cls.tile_chars.get(tile.properties.tile_type, cls.unknown_char)
                render += char
            render += '\n'
        print(render)
        return render

    @classmethod
    async def render_loop(cls, game_state: GameState, refresh_time_in_seconds=2):
        print("Starting ASCII render loop...")
        while True:
            cls.render(game_state)
            await asyncio.sleep(refresh_time_in_seconds)


class Arcade:

    def __init__(self, computer_inp):
        self.computer = IntcodeComputer(computer_inp)
        self.game_state = GameState()

    async def switch_on(self, is_part_2=True):
        print("Arcade is being switched on...")
        if is_part_2:
            # Bypass coin
            print("Apply coin patch...")
            self.computer.memory[0] = 2
        update_screen_task = asyncio.create_task(self.update_screen_data())
        print("Execute computer...")
        await self.computer.execute()
        print("Execution finished")
        print("Emptying output queue...")
        while not self.computer.output_queue.empty():
            await asyncio.sleep(0.01)
        print("Output queue is empty.")

    async def update_screen_data(self):
        print("Update screen data started...")
        while True:  # not self.computer.output_queue.empty():
            x = await self.computer.output_queue.get()
            y = await self.computer.output_queue.get()
            int_id = await self.computer.output_queue.get()
            if (x, y) == (-1, 0):
                self.game_state.score = int_id
            else:
                tile_id = TilesType(int_id)
                self.game_state.screen_data.add_tile(Tile(x, y, tile_id))


async def main_loop_part_1(inp):
    arcade = Arcade(inp)
    await arcade.switch_on(is_part_2=False)
    p1 = sum(tile.properties.tile_type is TilesType.BLOCK for tile in
             arcade.game_state.screen_data.get_tiles_as_dict().values())
    ScreenASCIIRender.render(arcade.game_state)
    return p1


async def main_loop_part_2(inp):
    AI_GAMER_INPUT_TIME_DELTA_IN_SECONDS = 0.01
    REFRESH_SCREEN_TIME_DELTA_IN_SECONDS = 1

    arcade = Arcade(inp)
    task_arcade_computer = asyncio.create_task(arcade.switch_on(is_part_2=True))
    task_player = asyncio.create_task(GamerAI.loop(arcade.game_state.screen_data, arcade.computer.input_queue,
                                                   refresh_time_in_seconds=AI_GAMER_INPUT_TIME_DELTA_IN_SECONDS))
    task_render = asyncio.create_task(
        ScreenASCIIRender.render_loop(arcade.game_state, refresh_time_in_seconds=REFRESH_SCREEN_TIME_DELTA_IN_SECONDS))
    await task_arcade_computer
    return arcade.game_state.score


class GamerAI:

    @staticmethod
    async def make_next_move(screen: ScreenData, move_queue: Queue):
        ball_tiles: List[Tile] = [tile for tile in screen.tiles.values() if tile.properties.tile_type is TilesType.BALL]
        paddle_tiles: List[Tile] = [tile for tile in screen.tiles.values() if
                                    tile.properties.tile_type is TilesType.PADDLE]
        if not ball_tiles or not paddle_tiles:
            print("No data")
            joystick_input = 0
        else:
            joystick_input = GamerAI.get_joystick_position(ball_tiles[0], paddle_tiles[0])
        # print(f"GamerAI: {joystick_input}")
        await move_queue.put(joystick_input)

    @staticmethod
    def get_joystick_position(ball_tile: Tile, paddle_tile: Tile):
        delta_x = ball_tile.location.x - paddle_tile.location.x
        if delta_x == 0:
            joystick_input = 0
        else:
            joystick_input = delta_x // abs(delta_x)
        return joystick_input

    @classmethod
    async def loop(cls, screen: ScreenData, move_queue: Queue, refresh_time_in_seconds=0.01):
        print("Gamer AI started")
        while True:
            await cls.make_next_move(screen, move_queue)
            await asyncio.sleep(refresh_time_in_seconds)


def part_1(inp):
    return asyncio.run(main_loop_part_1(inp))


def part_2(inp):
    return asyncio.run(main_loop_part_2(inp))


if __name__ == "__main__":
    print('*** solving main ***')
    main("input")
