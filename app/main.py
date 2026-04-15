# Entry point: app lifecycle, action dispatch.
# UI primitives live in app/ui/, queries live in app/queries.py.

import curses
import time

from app import queries
from app.ui.primitives import init_colors, box_width, draw_box, safe_addstr
from app.ui.screens import splash, render_menu, show_status, pause
from app.ui.input import get_command
from app.ui.theme import PAIR_DEFAULT


# Actions
def test_connection_action(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    w = box_width(stdscr)
    x = (cols - w) // 2
    y = max(1, rows // 2 - 4)

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


ACTIONS = {
    "1": test_connection_action,
}


# App lifecycle
def main(stdscr):
    curses.curs_set(0)
    init_colors()
    stdscr.bkgd(" ", curses.color_pair(PAIR_DEFAULT))

    splash(stdscr)
    while True:
        prompt_y, prompt_x = render_menu(stdscr)
        choice = get_command(stdscr, prompt_y, prompt_x)
        if choice == "0":
            return
        action = ACTIONS.get(choice)
        if action is None:
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4,
                        "UNKNOWN COMMAND. CONSULT MANUAL.", "err")
            time.sleep(0.8)
            continue
        action(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)