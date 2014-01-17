import random
import curses

import fov.player
import fov.shadowcasting

SIGHT_RANGE = 10

class VisibilityMap:
    def __init__ (self, height, width, sight_block_map, player, screen):
        self.height = height
        self.width = width
        self.sight_block_map = sight_block_map
        self.player = player
        self.internal_map = []
        for y in range (height):
            self.internal_map.append ([False for x in range (width)])
        self.compute_visibility (screen)

    def compute_visibility (self, screen):
        fov.shadowcasting.compute (self)

    def transform (self, point):
        y, x = point
        return (y + self.player.y, x + self.player.x)

    def is_visible (self, point):
        return self [self.transform (point)]

    def set_visible (self, point, value):
        self [self.transform (point)] = value

    def __iter__ (self):
        for y in range (self.height):
            for x in range (self.width):
                yield y, x, self [y, x]

    def __getitem__ (self, index):
        if isinstance (index, tuple):
            y, x = index
            return self.internal_map [y][x]
        else:
            raise IndexError ("VisibilityMap index must be a tuple")

    def __setitem__ (self, index, value):
        if isinstance (index, tuple):
            y, x = index
            self.internal_map [y][x] = value
        else:
            raise IndexError ("VisibilityMap index must be a tuple")

class SightBlockMap:
    def __init__ (self, map_or_function):
        self.map_or_function = map_or_function

    def __getitem__ (self, index):
        if isinstance (index, tuple):
            y, x = index
            try:
                return self.map_or_function [y][x]
            except TypeError:
                return self.map_or_function (y, x)
        else:
            raise IndexError ("SightBlockMap index must be a tuple")
