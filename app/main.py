# Entry point: app lifecycle, action dispatch.
# UI primitives live in app/ui/, queries live in app/queries.py.
import curses
import time

from app import queries
from app.ui.primitives import init_colors, box_width, draw_box, safe_addstr
from app.ui.screens import (
    splash, render_main_menu,
    render_manager_login_menu, render_client_login_menu,
    render_manager_menu, render_client_menu,
    render_manual, show_status, show_placeholder, pause,
)
from app.ui.input import get_command
from app.ui.theme import PAIR_DEFAULT, QUIT_CMDS, ERROR_UNKNOWN_COMMAND

# Actions
def test_connection_action(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    w = box_width(stdscr)
    x = (cols - w) // 2
    y = max(1, rows // 2 - 4)

    # a bunch of filler, might be fun to make this actually mean something idk
    draw_box(stdscr, y, x, w, 5, "DATABASE LINK TEST")
    safe_addstr(stdscr, y + 2, x + 4, "DIALING POSTGRES BACKEND ...",
                curses.color_pair(PAIR_DEFAULT))
    stdscr.refresh()

    try:
        version = queries.ping()
        show_status(stdscr, y + 6, x, f"LINK ESTABLISHED. {version}", "ok")
    except Exception as e:
        show_status(stdscr, y + 6, x, f"LINK DOWN: {e}", "err")
    pause(stdscr)


# Auth flow (just raw ssn as auth lmao)
def manager_access(stdscr):
    while True:
        prompt_y, prompt_x = render_manager_login_menu(stdscr)
        choice = get_command(stdscr, prompt_y, prompt_x)

        if choice in QUIT_CMDS:
            return

        if choice == "1":
            # TODO: draw_form for SSN, query manager, return record
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4, "todo", "warn")
            curses.flushinp()
            stdscr.getch()

        elif choice == "2":
            # TODO: draw_form for name/SSN/email, insert manager
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4, "todo", "warn")
            curses.flushinp()
            stdscr.getch()

        else:
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4, ERROR_UNKNOWN_COMMAND, "err")
            curses.flushinp()
            stdscr.getch()


def client_access(stdscr):
    while True:
        prompt_y, prompt_x = render_client_login_menu(stdscr)
        choice = get_command(stdscr, prompt_y, prompt_x)

        if choice in QUIT_CMDS:
            return

        if choice == "1":
            # TODO: draw_form for email, query client, return record
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4, "todo", "warn")
            curses.flushinp()
            stdscr.getch()

        elif choice == "2":
            # TODO: draw_form for name/email/address/card, insert client
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4, "todo", "warn")
            curses.flushinp()
            stdscr.getch()

        else:
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4, ERROR_UNKNOWN_COMMAND, "err")
            curses.flushinp()
            stdscr.getch()


def manual_action(stdscr):
    render_manual(stdscr)


# Sub-loops for each role
def manager_loop(stdscr):
    while True:
        prompt_y, prompt_x = render_manager_menu(stdscr)
        choice = get_command(stdscr, prompt_y, prompt_x)
        if choice in QUIT_CMDS:
            return
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, "todo", "warn")
        curses.flushinp()
        stdscr.getch()


def client_loop(stdscr):
    while True:
        prompt_y, prompt_x = render_client_menu(stdscr)
        choice = get_command(stdscr, prompt_y, prompt_x)
        if choice in QUIT_CMDS:
            return
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, "todo", "warn")
        curses.flushinp()
        stdscr.getch()


# App lifecycle
def main(stdscr):
    curses.curs_set(0)
    curses.mousemask(0)
    init_colors()
    stdscr.bkgd(" ", curses.color_pair(PAIR_DEFAULT))

    splash(stdscr)
    while True:
        prompt_y, prompt_x = render_main_menu(stdscr)
        choice = get_command(stdscr, prompt_y, prompt_x)

        if choice in QUIT_CMDS:
            return
        if choice == "1":
            test_connection_action(stdscr)
        elif choice == "2":
            manager_access(stdscr)
        elif choice == "3":
            client_access(stdscr)
        elif choice == "4":
            manual_action(stdscr)
        else:
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4, ERROR_UNKNOWN_COMMAND, "err")
            curses.flushinp()
            stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)