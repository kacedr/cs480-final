# Composed screens: splash, main menu, status messages, pause.
import curses
import time

from app.ui.theme import (
    PAIR_DEFAULT, PAIR_BORDER, PAIR_TITLE, PAIR_OK, PAIR_ERR,
    PAIR_WARN, PAIR_INFO, PAIR_DIM,
    BANNER, SUBTITLE, COPYRIGHT, TERMINAL,
    MAIN_MENU_ITEMS, MANAGER_LOGIN_ITEMS, CLIENT_LOGIN_ITEMS,
    MANAGER_MENU_ITEMS, CLIENT_MENU_ITEMS,
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

# generic scrollable menu rendering, could probably merge this with manual menu  rendering but oh well
def render_menu(stdscr, title, items, status_line=""):
    """
    Scrollable menu. Handles its own input loop.
    Returns the key string of the selected item, or None if user backed out.
    """
    from app.ui.theme import QUIT_CMDS
    from app.ui.input import get_command

    scroll = 0

    while True:
        stdscr.clear()
        rows, cols = stdscr.getmaxyx()
        w = box_width(stdscr)
        x = (cols - w) // 2

        # Reserve: title row, top border, bottom border, separator+status, prompt row, padding
        reserved = 7
        visible = max(3, rows - reserved)
        total = len(items)
        needs_scroll = total > visible
        shown = min(visible, total)

        h = shown + 5   # top border + blank + items + separator + status + bottom
        y = max(1, (rows - h - 2) // 2)

        max_scroll = max(0, total - shown)
        scroll = max(0, min(scroll, max_scroll))

        draw_box(stdscr, y, x, w, h, title)

        # Draw visible items
        for i in range(shown):
            idx = scroll + i
            if idx >= total:
                break
            key, label, color = items[idx]
            row = y + 2 + i
            safe_addstr(stdscr, row, x + 4, f"[{key}]",
                        curses.color_pair(color))
            safe_addstr(stdscr, row, x + 4 + len(key) + 3, label,
                        curses.color_pair(PAIR_DEFAULT))

        # Scroll indicators
        if needs_scroll:
            if scroll > 0:
                safe_addstr(stdscr, y + 1, x + w - 4, "▲",
                            curses.color_pair(PAIR_WARN) | curses.A_BOLD)
            if scroll < max_scroll:
                safe_addstr(stdscr, y + h - 3, x + w - 4, "▼",
                            curses.color_pair(PAIR_WARN) | curses.A_BOLD)
            indicator = f" {scroll + 1}-{scroll + shown}/{total} "
            safe_addstr(stdscr, y, x + w - len(indicator) - 4, indicator,
                        curses.color_pair(PAIR_DIM) | curses.A_DIM)

        draw_separator(stdscr, y + h - 2, x, w)

        if status_line:
            safe_addstr(stdscr, y + h - 1,
                        x + (w - len(status_line)) // 2 - 1,
                        status_line,
                        curses.color_pair(PAIR_OK) | curses.A_DIM)

        prompt_y = y + h + 1
        safe_addstr(stdscr, prompt_y, x, "command> ",
                    curses.color_pair(PAIR_OK) | curses.A_BOLD)
        stdscr.refresh()

        # Peek for scroll keys without entering command mode
        stdscr.nodelay(False)
        ch = stdscr.getch()

        # Scroll keys
        if ch in (ord("j"), curses.KEY_DOWN):
            scroll += 1
            continue
        if ch in (ord("k"), curses.KEY_UP):
            scroll -= 1
            continue
        if ch == curses.KEY_NPAGE:
            scroll += visible // 2
            continue
        if ch == curses.KEY_PPAGE:
            scroll -= visible // 2
            continue
        if ch == ord("g"):
            scroll = 0
            continue
        if ch == ord("G"):
            scroll = max_scroll
            continue

        # Anything else — push it back and let get_command handle it
        curses.ungetch(ch)
        choice = get_command(stdscr, prompt_y, x + 9)
        return choice

# Display a table of results in a box. Blocks until user hits enter.
def render_table(stdscr, title, headers, rows):
    stdscr.clear()
    scr_rows, scr_cols = stdscr.getmaxyx()

    # Compute column widths from headers and data
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Total width: sum of cols + separators (" | ") + box padding
    table_width = sum(col_widths) + 3 * (len(headers) - 1)
    w = min(max(table_width + 6, 40), scr_cols - 2)

    h = len(rows) + 6
    y = max(1, (scr_rows - h) // 2)
    x = (scr_cols - w) // 2

    draw_box(stdscr, y, x, w, h, title)

    # Header row
    header_line = "   ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    safe_addstr(stdscr, y + 2, x + 3, header_line,
                curses.color_pair(PAIR_TITLE) | curses.A_BOLD)

    # Separator under headers
    sep = "─" * len(header_line)
    safe_addstr(stdscr, y + 3, x + 3, sep,
                curses.color_pair(PAIR_BORDER))

    # Data rows
    for i, row in enumerate(rows):
        line = "   ".join(str(cell).ljust(col_widths[j]) for j, cell in enumerate(row))
        safe_addstr(stdscr, y + 4 + i, x + 3, line,
                    curses.color_pair(PAIR_DEFAULT))

    if not rows:
        safe_addstr(stdscr, y + 4, x + 3, "[ NO RESULTS ]",
                    curses.color_pair(PAIR_WARN) | curses.A_BOLD)

    stdscr.refresh()
    pause(stdscr)

# Specific menus
def render_main_menu(stdscr):
    return render_menu(
        stdscr, "MAIN MENU", MAIN_MENU_ITEMS,
        "STATUS: ONLINE   USER: GUEST   SESSION: ACTIVE",
    )


def render_manager_login_menu(stdscr):
    return render_menu(
        stdscr, "MANAGER ACCESS", MANAGER_LOGIN_ITEMS,
    )


def render_client_login_menu(stdscr):
    return render_menu(
        stdscr, "CLIENT ACCESS", CLIENT_LOGIN_ITEMS,
    )


def render_manager_menu(stdscr, name="MANAGER"):
    return render_menu(
        stdscr, "MANAGER CONSOLE", MANAGER_MENU_ITEMS,
        f"STATUS: ONLINE   USER: {name.upper()}   ROLE: MANAGER",
    )


def render_client_menu(stdscr, name="CLIENT"):
    return render_menu(
        stdscr, "CLIENT CONSOLE", CLIENT_MENU_ITEMS,
        f"STATUS: ONLINE   USER: {name.upper()}   ROLE: CLIENT",
    )


def render_manual(stdscr):
    MANUAL_LINES = [
        ("NAVIGATION",                                  PAIR_TITLE,  True),
        ("  [0] / :q / quit ........... BACK / DISCONNECT",     PAIR_DEFAULT, False),
        ("  [1-9]                       SELECT OPTION",         PAIR_DEFAULT, False),
        ("",                                                    PAIR_DEFAULT, False),
        ("ROLES",                                               PAIR_TITLE,   True),
        ("  MANAGER .................. HOTELS, ROOMS, REPORTS", PAIR_DEFAULT, False),
        ("  CLIENT ................... SEARCH, BOOK, REVIEW",   PAIR_DEFAULT, False),
        ("",                                                    PAIR_DEFAULT, False),
        ("MANAGER CAN",                                         PAIR_TITLE,   True),
        ("  [1]  INSERT HOTEL",                                 PAIR_DEFAULT, False),
        ("  [2]  INSERT ROOM",                                  PAIR_DEFAULT, False),
        ("  [3]  UPDATE HOTEL",                                 PAIR_DEFAULT, False),
        ("  [4]  UPDATE ROOM",                                  PAIR_DEFAULT, False),
        ("  [5]  REMOVE HOTEL",                                 PAIR_DEFAULT, False),
        ("  [6]  REMOVE ROOM",                                  PAIR_DEFAULT, False),
        ("  [7]  REMOVE CLIENT",                                PAIR_DEFAULT, False),
        ("  [8]  TOP-K CLIENTS BY BOOKINGS",                    PAIR_DEFAULT, False),
        ("  [9]  ROOM BOOKING COUNTS",                          PAIR_DEFAULT, False),
        ("  [10] HOTEL STATISTICS",                             PAIR_DEFAULT, False),
        ("  [11] CLIENTS BY CITY PAIR",                         PAIR_DEFAULT, False),
        ("  [12] PROBLEMATIC HOTELS",                           PAIR_DEFAULT, False),
        ("  [13] CLIENT SPENDING REPORT",                       PAIR_DEFAULT, False),
        ("",                                                    PAIR_DEFAULT, False),
        ("CLIENT CAN",                                          PAIR_TITLE,   True),
        ("  [1]  UPDATE MY NAME",                               PAIR_DEFAULT, False),
        ("  [2]  MANAGE ADDRESSES",                             PAIR_DEFAULT, False),
        ("  [3]  MANAGE CREDIT CARDS",                          PAIR_DEFAULT, False),
        ("  [4]  SEARCH AVAILABLE ROOMS BY DATE",               PAIR_DEFAULT, False),
        ("  [5]  BOOK A ROOM (MANUAL)",                         PAIR_DEFAULT, False),
        ("  [6]  AUTO-BOOK",                                    PAIR_DEFAULT, False),
        ("  [7]  VIEW MY BOOKINGS",                             PAIR_DEFAULT, False),
        ("  [8]  WRITE REVIEW (MUST HAVE STAYED)",              PAIR_DEFAULT, False),
        ("",                                                    PAIR_DEFAULT, False),
        ("BOOKING RULES",                                       PAIR_TITLE,   True),
        ("  - DATE RANGE IS INCLUSIVE [START, END]",            PAIR_DEFAULT, False),
        ("  - NO OVERLAPPING BOOKINGS ON SAME ROOM",            PAIR_DEFAULT, False),
        ("  - END DATE MUST BE AFTER START DATE",               PAIR_DEFAULT, False),
        ("",                                                    PAIR_DEFAULT, False),
        ("REGISTRATION",                                        PAIR_TITLE,   True),
        ("  - MANAGERS REGISTER WITH NAME, SSN, EMAIL",         PAIR_DEFAULT, False),
        ("  - CLIENTS REGISTER WITH NAME, EMAIL,",              PAIR_DEFAULT, False),
        ("    ADDRESS(ES), AND CREDIT CARD(S)",                 PAIR_DEFAULT, False),
        ("  - CLIENT EMAIL MUST BE UNIQUE",                     PAIR_DEFAULT, False),
        ("  - CLIENTS MUST HAVE >= 1 ADDRESS & >= 1 CARD",      PAIR_DEFAULT, False),
    ]

    scroll = 0
    total = len(MANUAL_LINES)

    while True:
        stdscr.clear()
        rows, cols = stdscr.getmaxyx()
        w = box_width(stdscr)
        x = (cols - w) // 2

        # Reserve rows: 1 top border, 1 title, 1 bottom border, 2 footer
        visible = rows - 6
        max_scroll = max(0, total - visible)
        scroll = max(0, min(scroll, max_scroll))

        draw_box(stdscr, 0, x, w, rows - 2, "SYSTEM MANUAL")

        # Draw visible portion
        for i in range(visible):
            idx = scroll + i
            if idx >= total:
                break
            text, pair, bold = MANUAL_LINES[idx]
            attr = curses.color_pair(pair)
            if bold:
                attr |= curses.A_BOLD
            safe_addstr(stdscr, 2 + i, x + 3, text, attr)

        # Scroll indicator
        if total > visible:
            pct = int((scroll / max_scroll) * 100) if max_scroll > 0 else 100
            indicator = f" LINE {scroll + 1}-{min(scroll + visible, total)} OF {total}  ({pct}%) "
            safe_addstr(stdscr, rows - 3, x + w - len(indicator) - 2,
                        indicator, curses.color_pair(PAIR_DIM) | curses.A_DIM)

        # Footer
        footer = "j/k  SCROLL   q/0  BACK"
        safe_addstr(stdscr, rows - 2, (cols - len(footer)) // 2,
                    footer, curses.color_pair(PAIR_DIM) | curses.A_DIM)

        stdscr.refresh()

        # Input
        ch = stdscr.getch()
        if ch in (ord("q"), ord("0")):
            return
        elif ch in (ord("j"), curses.KEY_DOWN):
            scroll += 1
        elif ch in (ord("k"), curses.KEY_UP):
            scroll -= 1
        elif ch in (ord("d"), curses.KEY_NPAGE):   # half-page down
            scroll += visible // 2
        elif ch in (ord("u"), curses.KEY_PPAGE):   # half-page up
            scroll -= visible // 2
        elif ch in (ord("g"),):                     # top
            scroll = 0
        elif ch in (ord("G"),):                     # bottom
            scroll = max_scroll


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


def show_placeholder(stdscr, y, x):
    safe_addstr(stdscr, y, x, "todo", curses.color_pair(PAIR_WARN) | curses.A_BOLD)
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