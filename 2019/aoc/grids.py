import dataclasses
from typing import Dict, Tuple, Callable, Iterable, Union

import numpy as np
from matplotlib import pyplot as plt

Coordinates = Tuple
Number = Union[int, float]
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

    def y_range_reversed(self) -> Iterable[int]:
        yield from range(self.y_max, self.y_min - 1, -1)

    @property
    def shape_reversed(self):
        return (self.y_max - self.y_min + 1, self.x_max - self.x_min + 1)


class UnstructuredGrid:
    def __init__(self, data_dict: Dict[Coordinates, CellData]):
        self._data_dict = data_dict

    def render_ascii(
        self, map_function: Callable[[CellData], ASCIIChar], missing_cell_char: str
    ):
        render: str = ""
        tiles_as_dict = self._data_dict
        limits = self.get_min_max_tile_coords()
        for y in limits.y_range_reversed():
            for x in limits.x_range():
                if not (x, y) in self._data_dict:
                    char = missing_cell_char
                else:
                    tile_object = tiles_as_dict[(x, y)]
                    char = map_function(tile_object)
                render += char
            render += "\n"
        print(render)
        return render

    def display_as_plot(
        self,
        map_function: Callable[[CellData], Number],
        missing_cell_number: Number = -1,
        animate_pause=None,
    ):
        range = self.get_min_max_tile_coords()
        np_array = np.full(range.shape_reversed, missing_cell_number)
        for coords, cell_data in self._data_dict.items():
            row = range.y_max - coords[1]
            col = coords[0] - range.x_min
            np_array[row, col] = map_function(cell_data)
        plt.clf()
        plt.imshow(np_array)
        plt.draw()
        if animate_pause is not None:
            plt.pause(animate_pause)

    def get_min_max_tile_coords(self) -> CoordRanges2D:
        limits = CoordRanges2D(
            x_min=9999999, x_max=-9999999, y_min=9999999, y_max=-9999999
        )
        for x, y in self._data_dict:
            limits.x_min = min(limits.x_min, x)
            limits.x_max = max(limits.x_max, x)
            limits.y_min = min(limits.y_min, y)
            limits.y_max = max(limits.y_max, y)
        return limits
