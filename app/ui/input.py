# Input helpers
import curses
from app.ui.primitives import safe_addstr, box_width, draw_box
from app.ui.theme import PAIR_DEFAULT, PAIR_TITLE, PAIR_DIM, PAIR_BORDER, PAIR_OK


def get_command(stdscr, y, x, max_len=8):
    """Read a short command, ignoring mouse/scroll garbage."""
    curses.curs_set(1)
    stdscr.move(y, x)
    buf = []

    while True:
        ch = stdscr.getch()

        if ch in (10, 13, curses.KEY_ENTER):
            break
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if buf:
                buf.pop()
                safe_addstr(stdscr, y, x + len(buf), " ",
                            curses.color_pair(PAIR_DEFAULT))
                stdscr.move(y, x + len(buf))
        elif ch == 27:
            stdscr.nodelay(True)
            while stdscr.getch() != -1:
                pass
            stdscr.nodelay(False)
        elif 32 <= ch <= 126:
            if len(buf) < max_len:
                buf.append(chr(ch))
                safe_addstr(stdscr, y, x + len(buf) - 1, chr(ch),
                            curses.color_pair(PAIR_DEFAULT))

        stdscr.refresh()

    curses.curs_set(0)
    return "".join(buf).strip()


def get_field(stdscr, y, x, max_len=64):
    """Read a longer field, same filtering as get_command."""
    return get_command(stdscr, y, x, max_len)


def draw_form(stdscr, title, fields):
    """
    Draw a titled box with labeled input fields and collect values.

    fields: list of (label, max_len) tuples
            e.g. [("NAME", 64), ("EMAIL", 128), ("SSN", 9)]

    Returns: list of entered strings in the same order,
             or None if user submits empty first field (cancel).
    """
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    w = box_width(stdscr)
    h = len(fields) * 2 + 4
    y = max(1, (rows - h) // 2)
    x = (cols - w) // 2

    draw_box(stdscr, y, x, w, h, title)

    max_label = max(len(f[0]) for f in fields)
    values = []

    for i, (label, max_len) in enumerate(fields):
        row = y + 2 + (i * 2)
        label_padded = label.ljust(max_label)
        safe_addstr(stdscr, row, x + 3, label_padded + " : ",
                    curses.color_pair(PAIR_TITLE))
        input_x = x + 3 + max_label + 3
        avail = w - (max_label + 9)
        field_len = min(avail, max_len)
        safe_addstr(stdscr, row, input_x, "_" * field_len,
                    curses.color_pair(PAIR_DIM) | curses.A_DIM)
        stdscr.refresh()

        val = get_field(stdscr, row, input_x, field_len)
        values.append(val)

    if not values[0]:
        return None
    return values


def draw_repeating_form(stdscr, title, fields, prompt_more="ADD ANOTHER?"):
    """
    Collect one or more sets of fields. After each set, asks if the user
    wants to add another. Returns a list of value-lists.

    fields: list of (label, max_len) tuples
    Returns: list of lists, e.g. [["123 Main", "5", "Chicago"], ["456 Oak", "10", "Denver"]]
             or None if user cancels on the first entry.
    """
    entries = []
    while True:
        stdscr.clear()
        rows, cols = stdscr.getmaxyx()
        w = box_width(stdscr)

        # Show count if we already have entries
        display_title = title
        if entries:
            display_title = f"{title} (#{len(entries) + 1})"

        vals = draw_form(stdscr, display_title, fields)
        if vals is None:
            if not entries:
                return None
            break
        entries.append(vals)

        # Ask if they want to add another
        rows, cols = stdscr.getmaxyx()
        y = rows // 2 + len(fields) + 2
        x = (cols - box_width(stdscr)) // 2
        safe_addstr(stdscr, y, x + 3, f"{prompt_more}  [Y/N] ",
                    curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
        stdscr.refresh()

        while True:
            ch = stdscr.getch()
            if ch in (ord("y"), ord("Y")):
                break
            if ch in (ord("n"), ord("N")):
                return entries

    return entries


def confirm(stdscr, message):
    """Show a Y/N confirmation prompt. Returns True for Y, False for N."""
    rows, cols = stdscr.getmaxyx()
    w = box_width(stdscr)
    x = (cols - w) // 2
    y = rows // 2

    safe_addstr(stdscr, y, x, message + "  [Y/N] ",
                curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    stdscr.refresh()

    while True:
        ch = stdscr.getch()
        if ch in (ord("y"), ord("Y")):
            return True
        if ch in (ord("n"), ord("N")):
            return False