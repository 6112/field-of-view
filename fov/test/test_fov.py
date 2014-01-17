import fov.map
import fov.player

import unittest
import curses

HEIGHT = 40
WIDTH = 40

SIGHT_RANGE = 10

class TestFoV (unittest.TestCase):
    def setUp (self):
        self.screen = open_screen ()
        self.player = fov.player.Player (HEIGHT // 2, WIDTH // 2)
        ground_tile = fov.map.Tile ('.', False, True)
        wall_tile = fov.map.Tile ('#', True, False)
        map_list = []
        for y in range (HEIGHT):
            map_list.append ([None for x in range (WIDTH)])
        for y in range (HEIGHT):
            map_list [y][0] = wall_tile
            map_list [y][WIDTH - 1] = wall_tile
        for x in range (WIDTH):
            map_list [0][x] = wall_tile
            map_list [HEIGHT - 1][x] = wall_tile
        walls = [(14, 13), (14, 14), (14, 15),
                 (15, 13), (15, 14), (15, 15),
                 (16, 13), (16, 14), (16, 15), (16, 18), (16, 21), (16, 22),
                 (17, 13), (17, 14)]
        for y, x in walls:
            map_list [y][x] = wall_tile
        self.world_map = fov.map.WorldMap (map_list, ground_tile)

    def test_fov (self):
        key = None
        while key != 'q':
            field_of_view = self.world_map.get_field_of_view (self.player,
              SIGHT_RANGE)
            render (self.screen, self.world_map, field_of_view, self.player)
            key = self.screen.getch ()
            try:
                key = chr (key)
            except ValueError:
                pass
            move_player (self.player, self.world_map, key)

    def tearDown (self):
        close_screen (self.screen)

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

def render (screen, world_map, field_of_view, player):
    for y in range (HEIGHT):
        for x in range (HEIGHT):
            is_visible = field_of_view [y, x]
            tile_char = world_map [y, x].display_character
            screen.addstr (y, x, tile_char, curses.A_REVERSE if is_visible
              else 0)
    screen.addstr (player.y, player.x, '@', curses.A_REVERSE)
    screen.addstr (HEIGHT + 1, 3, "Use hjkl to move around.")

def open_screen ():
    screen = curses.initscr ()
    curses.noecho ()
    curses.cbreak ()
    screen.keypad (1)
    return screen

def close_screen (screen):
    curses.nocbreak ()
    screen.keypad (0)
    curses.echo ()
    curses.endwin ()

if __name__ == "__main__":
    unittest.main ()
