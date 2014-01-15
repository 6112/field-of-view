import fov.map
import unittest
import curses

class TestFoV (unittest.TestCase):
    def setUp ():
        screen = open_screen ()

    def test_fov:
        screen.addstr (3, 3, "hello world")
        screen.getch ()

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
