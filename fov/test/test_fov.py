import fov.map
import fov.player

import fov.test.utils.curses as cursesutils

import unittest
import curses

HEIGHT = 40
WIDTH = 40

SIGHT_RANGE = 10

GROUND_TILE = fov.map.Tile ('.', False, True)
WALL_TILE = fov.map.Tile ('#', True, False)

class TestFoV (unittest.TestCase):
    def setUp (self):
        self.screen = cursesutils.open_screen ()
        self.player = fov.player.Player (HEIGHT // 2, WIDTH // 2)
        self.world_map = create_map ()

    def test_fov (self):
        key = None
        while key != 'q':
            field_of_view = self.world_map.get_field_of_view (self.player,
              SIGHT_RANGE)
            cursesutils.render (self.screen, self.world_map, field_of_view, 
              self.player)
            key = self.screen.getch ()
            try:
                key = chr (key)
            except ValueError:
                pass
            move_player (self.player, self.world_map, key)

    def tearDown (self):
        cursesutils.close_screen (self.screen)

def move_player (player, world_map, key):
    dy = 0
    dx = 0
    if key == 'h':
        dx = -1
    elif key == 'j':
        dy = 1
    elif key == 'k':
        dy = -1
    elif key == 'l':
        dx = 1
    elif key == 'y':
        dy = -1
        dx = -1
    elif key == 'u':
        dy = -1
        dx = 1
    elif key == 'b':
        dy = 1
        dx = -1
    elif key == 'n':
        dy = 1
        dx = 1
    player.y += dy
    player.x += dx
    if not world_map [player.y, player.x].walkable:
        player.y -= dy
        player.x -= dx

def create_map ():
    map_list = []
    for y in range (HEIGHT):
        map_list.append ([None for x in range (WIDTH)])
    for y in range (HEIGHT):
        map_list [y][0] = WALL_TILE
        map_list [y][WIDTH - 1] = WALL_TILE
    for x in range (WIDTH):
        map_list [0][x] = WALL_TILE
        map_list [HEIGHT - 1][x] = WALL_TILE
    walls = [(14, 13), (14, 14), (14, 15),
             (15, 13), (15, 14), (15, 15),
             (16, 13), (16, 14), (16, 15), (16, 18), (16, 21), (16, 22),
             (17, 13), (17, 14)]
    for y, x in walls:
        map_list [y][x] = WALL_TILE
    return fov.map.WorldMap (map_list, GROUND_TILE)

if __name__ == "__main__":
    unittest.main ()
