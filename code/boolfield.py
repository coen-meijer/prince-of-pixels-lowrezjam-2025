from __future__ import annotations

import pygame
import pygame.surfarray as surfarray
import numpy as np

class BoolField:

    def __init__(self, array):
        self.array = array

    def logical_and(self, other)  -> "BoolField":
        return BoolField(np.logical_and(self.array, other.array))

    def logical_or(self, other) -> "BoolField":
        return BoolField(np.logical_or(self.array, other.array))

    def logical_xor(self, other) -> "BoolField":
        return BoolField(np.logical_xor(self.array, other.array))

    def window(self, offset, shape) -> "BoolField":
        slice = self.array[ offset[0]:offset[0] + shape[0], offset[1]:offset[1] + shape[1]]
        return BoolField(slice)

    def negative(self) -> "BoolField":
        return BoolField(np.logical_not(self.array))

    def transpose(self) -> "BoolField":
        return BoolField(np.transpose(self.array))

    def count(self)  -> int:
        return np.count_nonzero(self.array)

    def find(self, pattern) -> list[tuple[int, int]]:
        debug = False
        matches = []
        self_rows, self_cols = self.array.shape
        pattern_rows, pattern_cols = pattern.array.shape

        for i in range(self_rows - pattern_rows + 1):
            for j in range(self_cols - pattern_cols + 1):
                area = self.array[j:j+pattern_cols, i:i+pattern_rows]   # colums first order!
                if debug:
                    print("_________________________________")
                    print(j, j)
                    print(area)
                    print(pattern)
                if np.array_equal(area, pattern.array):
                    matches.append((j,  i))  # colums first order!
                    print("recognizes pattern")

        return matches

        # np.array_less

    def size(self):
        return self.array.shape

    def exists(self)  -> bool:
        return self.array.any()

    def universal(self)  -> bool:
        return self.array.all()

# end of the class. Some functions to create BoolFields

def opaque(surf, threshold=128) -> BoolField:
    alpha = surfarray.pixels_alpha(surf)
    boolarray = alpha >= threshold
    return BoolField(surfarray.array_alpha(surf))

def transparent(surf, threshold=127) -> BoolField:
    boolarray = surfarray.pixels_alpha(surf) <= threshold
    return BoolField(boolarray)

def is_color(surf, color) -> BoolField:
    if isinstance(color, tuple):
        color_array = np.array(color)
        surface_colors = surfarray.pixels3d(surf)
        boolarray = np.all(surface_colors == color, axix=2)
    elif isinstance(color, int):
        boolarray = surfarray.pixels2d(surf) == color
    elif isinstance(color, str):
        if color[0] == '#':
            color = color[1:]
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        color_array = np.array([r, g, b])
        surface_colors = surfarray.pixels3d(surf)
        boolarray = np.all(surface_colors[0:3] == color and surface_colors[3] !=0, axix=2)
    return BoolField(boolarray)

def is_char(charfield, match_char) -> BoolField:
    if isinstance(charfield, str):
        lines = charfield.splitlines()
    else:
        lines = charfield
    horizontal = len(lines[0])
    vertical = len(lines)
    array = np.full((horizontal, vertical), False)
    for line_no, line in enumerate(lines):
        for col_no, character in enumerate(line):
            array[line_no, col_no] = (character == char)
    return BoolField(array)

def boolfieldtest():
     pattern = is_char(["***", "* *", "***"], '*')
     print(pattern.find(pattern))


