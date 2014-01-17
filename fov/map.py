import random
import curses

import fov.player
import fov.shadowcasting

class Tile:
    """An immutable tile type.
    
    Attributes:
        display_character: character used to draw this tile onto the screen.
        blocks_sight: True if this tile blocks sight.
        walkable: True if this tile is walkable.
    """

    def __init__ (self, display_character, blocks_sight, walkable):
        """Constructor for a Tile.

        Args:
            display_character: character used to draw this tile onto the screen.
            blocks_sight: True if this tile blocks sight.
            walkable: True if this tile is walkable.
        Raises:
            TypeError: if display_character is not a character
        """
        if not isinstance (display_character, str) or \
           len (display_character) != 1:
            raise TypeError ("display_character must be a character.")
        else:
            self.display_character = display_character
            self.blocks_sight = blocks_sight
            self.walkable = walkable

class WorldMap:
    """Object representing the world map.

    May be indexed like a list, with a tuple. Every element should be a Tile 
    object.

    Attributes:
        height: height of the map.
        width: width of the map.
        internal: internal 2-d list used to represent the map.
    """

    def __init__ (self, array, default_tile = None):
        """Constructor for a WorldMap.

        Args:
            array: a 2-dimensional list from which to construct the WorldMap.
            default_tile: tile to set the array elements that are equal to
                None. optional.
        Raises:
            TypeError: if array contains a non-Tile object.
        """
        self.height = len (array)
        self.width = len (array [0]) if self.height != 0 else 0
        self.internal = array
        for y in range (self.height):
            for x in range (self.width):
                if default_tile and not self.internal [y][x]:
                    self.internal [y][x] = default_tile
                if not isinstance (self.internal [y][x], Tile):
                    raise TypeError ("tile must be a Tile object.")

    def get_field_of_view (self, player, radius):
        """Return a list-like object that tells which tiles can be seen.

        Args:
            player: player whose field of view we want to know.
            radius: sight radius of the player.
        Returns:
            a FieldOfViewMap object which can be indexed like a WorldMap, and
            whose elements are True for visible tiles, and False for non-visible
            tiles.
        """
        return FieldOfViewMap (self, player, radius)

    def __getitem__ (self, point):
        """Get the value of a tile by coordinates.

        The coordinates should be a tuple, i.e.:

        world_map [y, x]

        Args:
            point: tuple representing the (y, x) coordinates of the tile.
        Returns:
            a Tile object representing the tile at the given point.
        Raises:
            IndexError: if point is not a tuple.
            IndexError: if one of the coordinates is not an integer.
            IndexError: if one of the coordinates is not inside the map.
        """
        if not isinstance (point, tuple):
            raise IndexError ("point must be a tuple.")
        else:
            y, x = point
            if not isinstance (y, int) or not isinstance (x, int):
                raise IndexError ("coordinates must be integers.")
            elif y < 0 or x < 0 or x >= self.width or y >= self.height:
                raise IndexError ("coordinates out of range.")
            else:
                return self.internal [y][x]

    def __setitem__ (self, point, tile):
        """Set the value of a tile by coordinates.

        The coordinates should be a tuple, i.e.:

        world_map [y, x] = tile

        Args:
            point: tuple representing the (y, x) coordinates of the tile.
            tile: new tile to use at the given position.
        Raises:
            IndexError: if point is not a tuple.
            IndexError: if one of the coordinates is not an integer.
            IndexError: if one of the coordinates is not inside the map.
            TypeError: if tile is not a Tile object.
        """
        if not isinstance (tile, Tile):
            raise TypeError ("tile must be a Tile object.")
        elif not isinstance (point, tuple):
            raise IndexError ("point must be a tuple.")
        else:
            y, x = point
            if not isinstance (y, int) or not isinstance (x, int):
                raise IndexError ("coordinates must be integers.")
            elif y < 0 or x < 0 or x >= height or y >= height:
                raise IndexError ("coordinates out of range.")
            else:
                self.internal [y][x] = tile

class FieldOfViewMap:
    """Represents which elements on the WorldMap can be seen by the player.
    
    May be accessed by a 2-d list to know whether a given tile is visible or
    not.

    Attributes:
        height: height of the map.
        width: width of the map.
    """

    def __init__ (self, world_map, player, radius):
        """Constructor for FieldOfViewMap.

        Args:
            world_map: WorldMap for which this FieldOfViewMap exists.
            player: entity whose field-of-view is calculated.
            radius: sight radius of the player entity.
        """
        self.world_map = world_map
        self.player = player
        self.radius = radius
        self.internal = []
        for y in range (world_map.height):
            self.internal.append ([False for x in range (world_map.width)])
        fov.shadowcasting.compute (self.world_map, self)

    def __getitem__ (self, point):
        """Get the visibility of a tile by coordinates.

        The coordinates should be a tuple, i.e.:

        visibility_map [y, x]

        Args:
            point: tuple representing the (y, x) coordinates of the tile.
        Returns:
            a Tile object representing the tile at the given point.
        Raises:
            IndexError: if point is not a tuple.
            IndexError: if one of the coordinates is not an integer.
            IndexError: if one of the coordinates is not inside the map.
        """
        if isinstance (point, tuple):
            y, x = point
            if not isinstance (y, int) or not isinstance (x, int):
                raise IndexError ("coordinates must be integers.")
            elif y < 0 or x < 0 or \
                 x >= self.world_map.width or y >= self.world_map.height:
                raise IndexError ("coordinates out of range.")
            else:
                return self.internal [y][x]
        else:
            raise IndexError ("index must be a tuple.")

    def __setitem__ (self, point, value):
        """Set the visibility of a tile by coordinates.

        Args:
            point: tuple representing the (y, x) coordinates of the point.
            value: True iff the tile should be visible.
        Raises:
            IndexError: if point is not a tuple.
        """
        if isinstance (point, tuple):
            y, x = point
            self.internal [y][x] = value
        else:
            raise IndexError ("index must be a tuple.")

class Octant:
    """Represents an octant with a given origin point.

    Attributes:
        index: index of this octant (0 to 7).
        origin: (y, x) origin of the octant.
        multipliers: dictionary of multipliers used for coordinate
        transformations.
    """

    # lists of dictionary values for transformations
    multipliers = {
        # x to x factors, for each octant
        "xx": [1,  0,  0, -1, -1,  0,  0,  1],
        # y to x factors, for each octant
        "yx": [0,  1, -1,  0,  0, -1,  1,  0],
        # x to y factors, for each octant
        "xy": [0,  1,  1,  0,  0, -1, -1,  0],
        # y to y factors, for each octant
        "yy": [1,  0,  0,  1, -1,  0,  0, -1]
    }

    def __init__ (self, index, origin = (0, 0)):
        """Constructor for an Octant.

        Args:
            index: index of this octant, starting at 0.
            origin: (y, x) origin of this octant. optional.
        Raises:
            TypeError: if index is not an integer.
            ValueError if index < 0 or index >= 8.
            TypeError: if origin is not a tuple.
            TypeError: if one of the coordinates or origin is not an integer.
        """
        if not isinstance (index, int):
            raise TypeError ("index must be an integer.")
        elif index < 0 or index >= 8:
            raise ValueError ("invalid octant index.")
        elif not isinstance (origin, tuple):
            raise TypeError ("origin must be a tuple.")
        elif not isinstance (origin [0], int) or \
             not isinstance (origin [1], int):
            raise TypeError ("origin coordinates must be integers.")
        else:
            self.multipliers = dict ((key, xs [index]) for key, xs in
                Octant.multipliers.items ())
            self.origin = origin

    def transformed_point (self, point):
        """Returns a transformed point from octant 0 to this octant.

        Args:
            point: (y, x) point to transform.
        Returns:
            a tuple representing the transformed point.
        Raises:
            TypeError: if point not a tuple.
            TypeError: if one of the coordinates of point is not an integer.
        """
        if not isinstance (point, tuple):
            raise TypeError ("point must be a tuple.")
        elif not isinstance (point [0], int) or \
             not isinstance (point [1], int):
            raise TypeError ("coordinates must be integers.")
        else:
            y, x = point
            transformed = \
              (x * self.multipliers ["xy"] + y * self.multipliers ["yy"],
               x * self.multipliers ["xx"] + y * self.multipliers ["yx"])
            transformed = \
              (transformed [0] + self.origin [0],
               transformed [1] + self.origin [1])
            return transformed
