# Drawing helpers
import curses
from app.ui.theme import (
    PAIR_DEFAULT, PAIR_BORDER, PAIR_TITLE, PAIR_OK, PAIR_ERR,
    PAIR_WARN, PAIR_INFO, PAIR_DIM,
    TL, TR, BL, BR, H, V, LT, RT,
)

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(PAIR_DEFAULT, curses.COLOR_WHITE,   -1)
    curses.init_pair(PAIR_BORDER,  curses.COLOR_CYAN,    -1)
    curses.init_pair(PAIR_TITLE,   curses.COLOR_YELLOW,  -1)
    curses.init_pair(PAIR_OK,      curses.COLOR_GREEN,   -1)
    curses.init_pair(PAIR_ERR,     curses.COLOR_RED,     -1)
    curses.init_pair(PAIR_WARN,    curses.COLOR_YELLOW,  -1)
    curses.init_pair(PAIR_INFO,    curses.COLOR_CYAN,    -1)
    curses.init_pair(PAIR_DIM,     curses.COLOR_WHITE,   -1)


def safe_addstr(stdscr, y, x, text, attr=0):
    # addstr that won't crash on edge-of-screen writes
    try:
        stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass


def box_width(stdscr):
    _, cols = stdscr.getmaxyx()
    return max(40, min(cols - 2, 100))


def center_x(stdscr, text):
    _, cols = stdscr.getmaxyx()
    return max(0, (cols - len(text)) // 2)


def draw_box(stdscr, y, x, w, h, title=""):
    border = curses.color_pair(PAIR_BORDER)
    safe_addstr(stdscr, y, x, TL + H * (w - 2) + TR, border)
    for i in range(1, h - 1):
        safe_addstr(stdscr, y + i, x, V, border)
        safe_addstr(stdscr, y + i, x + w - 1, V, border)
    safe_addstr(stdscr, y + h - 1, x, BL + H * (w - 2) + BR, border)
    if title:
        title_str = f" {title} "
        tx = x + (w - len(title_str)) // 2
        safe_addstr(stdscr, y, tx, title_str,
                    curses.color_pair(PAIR_TITLE) | curses.A_BOLD)


def draw_separator(stdscr, y, x, w):
    border = curses.color_pair(PAIR_BORDER)
    safe_addstr(stdscr, y, x, LT + H * (w - 2) + RT, border)