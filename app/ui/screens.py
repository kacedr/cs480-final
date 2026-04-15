# Composed screens: splash, main menu, status messages, pause.
# Built from primitives

import curses
import time

from app.ui.theme import (
    PAIR_DEFAULT, PAIR_BORDER, PAIR_TITLE, PAIR_OK, PAIR_ERR,
    PAIR_WARN, PAIR_INFO, PAIR_DIM,
    BANNER, SUBTITLE, COPYRIGHT, TERMINAL,
)
from app.ui.primitives import (
    safe_addstr, box_width, center_x, draw_box, draw_separator,
)


# Splash
def splash(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    y = max(1, (rows - 18) // 2)

    for line in BANNER:
        safe_addstr(stdscr, y, center_x(stdscr, line), line,
                    curses.color_pair(PAIR_BORDER) | curses.A_BOLD)
        y += 1
    y += 1
    safe_addstr(stdscr, y, center_x(stdscr, SUBTITLE), SUBTITLE,
                curses.color_pair(PAIR_TITLE))
    y += 2
    safe_addstr(stdscr, y, center_x(stdscr, COPYRIGHT), COPYRIGHT,
                curses.color_pair(PAIR_DIM) | curses.A_DIM)
    y += 1
    safe_addstr(stdscr, y, center_x(stdscr, TERMINAL), TERMINAL,
                curses.color_pair(PAIR_OK) | curses.A_DIM)
    y += 2
    stdscr.refresh()

    boot_lines = [
        "INITIALIZING DATABASE LINK ........",
        "LOADING RESERVATION KERNEL ........",
        "MOUNTING /dev/hotel ...............",
        "HANDSHAKE WITH POSTGRES ...........",
    ]
    boot_x = max(2, (cols - 50) // 2)
    for line in boot_lines:
        safe_addstr(stdscr, y, boot_x, line, curses.color_pair(PAIR_DEFAULT))
        stdscr.refresh()
        time.sleep(0.15)
        safe_addstr(stdscr, y, boot_x + len(line) + 1, "[",
                    curses.color_pair(PAIR_BORDER))
        safe_addstr(stdscr, y, boot_x + len(line) + 2, " OK ",
                    curses.color_pair(PAIR_OK) | curses.A_BOLD)
        safe_addstr(stdscr, y, boot_x + len(line) + 6, "]",
                    curses.color_pair(PAIR_BORDER))
        stdscr.refresh()
        y += 1

    y += 1
    msg = ">>> PRESS ENTER TO CONTINUE <<<"
    safe_addstr(stdscr, y, center_x(stdscr, msg), msg,
                curses.color_pair(PAIR_TITLE) | curses.A_BLINK)
    stdscr.refresh()

    while True:
        ch = stdscr.getch()
        if ch in (10, 13, curses.KEY_ENTER):
            break


# Main menu
MENU_ITEMS = [
    ("1", "TEST DATABASE CONNECTION", PAIR_TITLE),
    ("2", "MANAGER LOGIN",            PAIR_TITLE),
    ("3", "CLIENT LOGIN",             PAIR_TITLE),
    ("4", "REGISTER NEW CLIENT",      PAIR_TITLE),
    ("5", "REGISTER NEW MANAGER",     PAIR_TITLE),
    ("0", "DISCONNECT",               PAIR_ERR),
]


def render_menu(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    w = box_width(stdscr)
    h = len(MENU_ITEMS) + 7
    y = max(1, (rows - h) // 2)
    x = (cols - w) // 2

    draw_box(stdscr, y, x, w, h, "MAIN MENU")

    for i, (key, label, color) in enumerate(MENU_ITEMS):
        row = y + 2 + i
        if key == "0":
            row += 1   # gap before disconnect
        safe_addstr(stdscr, row, x + 4, f"[{key}]", curses.color_pair(color))
        safe_addstr(stdscr, row, x + 8, label, curses.color_pair(PAIR_DEFAULT))

    draw_separator(stdscr, y + h - 2, x, w)
    status_line = "STATUS: ONLINE   USER: GUEST   SESSION: ACTIVE"
    safe_addstr(stdscr, y + h - 1, x + (w - len(status_line)) // 2 - 1,
                status_line, curses.color_pair(PAIR_OK) | curses.A_DIM)

    prompt_y = y + h + 1
    safe_addstr(stdscr, prompt_y, x, "command> ",
                curses.color_pair(PAIR_OK) | curses.A_BOLD)
    stdscr.refresh()
    return prompt_y, x + 9


# Status / pause
def show_status(stdscr, y, x, msg, kind="info"):
    """kind: info | ok | err | warn"""
    tag = {
        "info": (PAIR_INFO,  "INFO"),
        "ok":   (PAIR_OK,    " OK "),
        "err":  (PAIR_ERR,   "FAIL"),
        "warn": (PAIR_WARN,  "WARN"),
    }[kind]
    pair, label = tag
    safe_addstr(stdscr, y, x, "[", curses.color_pair(PAIR_BORDER))
    safe_addstr(stdscr, y, x + 1, label,
                curses.color_pair(pair) | curses.A_BOLD)
    safe_addstr(stdscr, y, x + 5, "]", curses.color_pair(PAIR_BORDER))
    safe_addstr(stdscr, y, x + 7, msg, curses.color_pair(PAIR_DEFAULT))
    stdscr.refresh()


def pause(stdscr):
    rows, cols = stdscr.getmaxyx()
    msg = "-- press enter to return to menu --"
    safe_addstr(stdscr, rows - 2, (cols - len(msg)) // 2, msg,
                curses.color_pair(PAIR_DIM) | curses.A_DIM)
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ch in (10, 13, curses.KEY_ENTER):
            break