# Input helpers
import curses

def get_command(stdscr, y, x, max_len=8):
    """Read a short command string at (y, x) with cursor visible and echo on."""
    curses.curs_set(1)
    curses.echo()
    stdscr.move(y, x)
    try:
        raw = stdscr.getstr(y, x, max_len)
        return raw.decode("utf-8", errors="ignore").strip()
    finally:
        curses.noecho()
        curses.curs_set(0)


def get_field(stdscr, y, x, max_len=64):
    """Read a longer field (e.g., for registration forms)."""
    curses.curs_set(1)
    curses.echo()
    stdscr.move(y, x)
    try:
        raw = stdscr.getstr(y, x, max_len)
        return raw.decode("utf-8", errors="ignore").strip()
    finally:
        curses.noecho()
        curses.curs_set(0)