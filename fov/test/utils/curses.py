import curses

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

def render (screen, world_map, field_of_view, player):
    for y in range (world_map.height):
        for x in range (world_map.width):
            is_visible = field_of_view [y, x]
            tile_char = world_map [y, x].display_character
            screen.addstr (y, x, tile_char, curses.A_REVERSE if is_visible
              else 0)
    screen.addstr (player.y, player.x, '@', curses.A_REVERSE)
    screen.addstr (world_map.height + 1, 3, "Use hjkl to move around.")
