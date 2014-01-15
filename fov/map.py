import random

class VisibilityMap:
    def __init__ (self, height, width, sight_block_map):
        self.height = height
        self.width = width
        self.internal_map = []
        self.sight_block_map = sight_block_map
        for y in range (height):
            self.internal_map.append ([False for x in range (width)])
        self.compute_visibility ()

    def compute_visibility (self):
        if random.randint (0, 1) == 0:
            self [y, x] = True
        else:
            self [y, x] = False

    def __iter__ (self):
        for y in range (height):
            for x in range (width):
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
