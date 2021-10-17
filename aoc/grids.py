import dataclasses
from typing import Dict, Tuple, Callable, Iterable

Coordinates = Tuple
Number = [int, float]
CellData = object
ASCIIChar = str

@dataclasses.dataclass
class CoordRanges2D:
    x_min: Number
    x_max: Number
    y_min: Number
    y_max: Number

    def as_tuple(self):
        return ((self.x_min, self.x_max), (self.y_min, self.y_max))

    def x_range(self) -> Iterable[int]:
        yield from range(self.x_min, self.x_max + 1)

    def y_range(self) -> Iterable[int]:
        yield from range(self.y_min, self.y_max + 1)

class UnstructuredGrid:

    def __init__(self, data_dict: Dict[Coordinates, CellData]):
        self._data_dict = data_dict

    def render_ascii(self, map_function:Callable[[CellData], ASCIIChar], missing_cell_char: str):
        render: str = ""
        tiles_as_dict = self._data_dict
        limits = self.get_min_max_tile_coords()
        for y in limits.y_range():
            for x in limits.x_range():
                if not (x, y) in self._data_dict:
                    char = missing_cell_char
                else:
                    tile_object = tiles_as_dict[(x, y)]
                    char = map_function(tile_object)
                render += char
            render += '\n'
        print(render)
        return render

    def display_as_plot(self):
        ...

    def get_min_max_tile_coords(self) -> CoordRanges2D :
        limits = CoordRanges2D(x_min=9999999, x_max=-9999999, y_min=9999999, y_max=-9999999)
        for x, y in self._data_dict:
            limits.x_min = min(limits.x_min, x)
            limits.x_max = max(limits.x_max, x)
            limits.y_min = min(limits.y_min, y)
            limits.y_max = max(limits.y_max, y)
        return limits



