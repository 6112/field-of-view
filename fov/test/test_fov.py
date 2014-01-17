import fov.map
import fov.player

import unittest
import curses

HEIGHT = 40
WIDTH = 40

class TestFoV (unittest.TestCase):
    def setUp (self):
        self.screen = open_screen ()
        self.player = fov.player.Player (HEIGHT // 2, WIDTH // 2)
        self.map = []
        for y in range (HEIGHT):
            self.map.append ([0 for x in range (WIDTH)])
        for y in range (HEIGHT):
            self.map [y][0] = 1
            self.map [y][WIDTH - 1] = 1
        for x in range (WIDTH):
            self.map [0][x] = 1
            self.map [HEIGHT - 1][x] = 1
        walls = [(14, 13), (14, 14), (14, 15),
                 (15, 13), (15, 14), (15, 15),
                 (16, 13), (16, 14), (16, 15), (16, 18), (16, 21), (16, 22),
                 (17, 13), (17, 14)]
        for y,x in walls:
            self.map [y][x] = 1

    def test_fov (self):
        sight_block_map = fov.map.SightBlockMap (self.map)
        key = None
        while key != 'q':
            visibility_map = fov.map.VisibilityMap (HEIGHT, WIDTH,
              sight_block_map, self.player, self.screen)
            render (self.screen, self.map, visibility_map, self.player)
            key = self.screen.getch ()
            key = chr (key)
            move (self.player, self.map, key)

    def tearDown (self):
        close_screen (self.screen)

def move (player, map, key):
    dx = 0
    dy = 0
    if key == 'h':
        dx = -1
    elif key == 'j':
        dy = 1
    elif key == 'k':
        dy = -1
    elif key == 'l':
        dx = 1
    elif key == 'y':
        dx = -1
        dy = -1
    elif key == 'u':
        dx = 1
        dy = -1
    elif key == 'b':
        dx = -1
        dy = 1
    elif key == 'n':
        dx = 1
        dy = 1
    player.x += dx
    player.y += dy
    if map [player.y][player.x]:
        player.x -= dx
        player.y -= dy

def render (screen, map, visibility_map, player):
    for y in range (HEIGHT):
        for x in range (HEIGHT):
            is_visible = visibility_map [y, x]
            tile_char = '#' if map[y][x] else '.'
            screen.addstr (y, x, tile_char, curses.A_REVERSE if is_visible
              else 0)
    screen.addstr (player.y, player.x, '@')
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

if __name__ == '__main__':
    unittest.main ()
