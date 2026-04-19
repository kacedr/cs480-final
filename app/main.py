# Entry point
# UI primitives live in app/ui/, queries live in app/queries.py.
import curses
import time

from app import queries
from app.ui.primitives import init_colors, box_width, draw_box, safe_addstr
from app.ui.screens import (
    splash, render_main_menu,
    render_manager_login_menu, render_client_login_menu,
    render_manager_menu, render_client_menu,
    render_manual, render_table, show_status, show_placeholder, pause,
)
from app.ui.input import get_command, draw_form, draw_repeating_form, confirm
from app.ui.theme import PAIR_DEFAULT, QUIT_CMDS

# Actions
def test_connection_action(stdscr):
    """Test connection to postgres database"""
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


# Manager auth
def do_manager_login(stdscr):
    """Prompt for SSN, query DB, return (ssn, name, email) or None."""
    vals = draw_form(stdscr, "MANAGER LOGIN", [
        ("SSN (9 DIGITS)", 9),
    ])
    if not vals:
        return None

    ssn = vals[0]
    try:
        row = queries.manager_login(ssn)
    except Exception as e:
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, f"DB ERROR: {e}", "err")
        curses.flushinp()
        stdscr.getch()
        return None

    if row is None:
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, "SSN NOT FOUND.", "err")
        curses.flushinp()
        stdscr.getch()
        return None

    rows, _ = stdscr.getmaxyx()
    show_status(stdscr, rows - 3, 4, f"WELCOME BACK, {row[1].upper()}.", "ok")
    curses.flushinp()
    stdscr.getch()
    return row


def do_manager_register(stdscr):
    """Prompt for name/SSN/email, insert into DB, return row or None."""
    vals = draw_form(stdscr, "REGISTER NEW MANAGER", [
        ("NAME",           64),
        ("SSN (9 DIGITS)",  9),
        ("EMAIL",         128),
    ])
    if not vals:
        return None

    name, ssn, email = vals
    try:
        row = queries.register_manager(ssn, name, email)
    except Exception as e:
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, f"REGISTRATION FAILED: {e}", "err")
        curses.flushinp()
        stdscr.getch()
        return None

    rows, _ = stdscr.getmaxyx()
    show_status(stdscr, rows - 3, 4, f"MANAGER {name.upper()} REGISTERED.", "ok")
    curses.flushinp()
    stdscr.getch()
    return row


def manager_access(stdscr):
    """Login/register gate before the manager console."""
    while True:
        choice = render_manager_login_menu(stdscr)

        if choice in QUIT_CMDS:
            return

        if choice == "1":
            result = do_manager_login(stdscr)
            if result:
                manager_loop(stdscr, result)

        elif choice == "2":
            result = do_manager_register(stdscr)
            if result:
                manager_loop(stdscr, result)

        else:
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4,
                        "UNKNOWN COMMAND. CONSULT MANUAL.", "err")
            curses.flushinp()
            stdscr.getch()


# Client auth
def do_client_login(stdscr):
    """Prompt for email, query DB, return (client_id, name, email) or None."""
    vals = draw_form(stdscr, "CLIENT LOGIN", [
        ("EMAIL", 128),
    ])
    if not vals:
        return None

    email = vals[0]
    try:
        row = queries.client_login(email)
    except Exception as e:
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, f"DB ERROR: {e}", "err")
        curses.flushinp()
        stdscr.getch()
        return None

    if row is None:
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, "EMAIL NOT FOUND.", "err")
        curses.flushinp()
        stdscr.getch()
        return None

    rows, _ = stdscr.getmaxyx()
    show_status(stdscr, rows - 3, 4, f"WELCOME BACK, {row[1].upper()}.", "ok")
    curses.flushinp()
    stdscr.getch()
    return row


def do_client_register(stdscr):
    """
    Multi-step registration:
    1. Name + email
    2. One or more addresses
    3. One or more credit cards (each with billing address)
    """
    # Step 1: basic info
    basic = draw_form(stdscr, "REGISTER CLIENT (1/3) - INFO", [
        ("NAME",  64),
        ("EMAIL", 128),
    ])
    if not basic:
        return None
    name, email = basic

    # Step 2: addresses (at least one required)
    addresses = draw_repeating_form(
        stdscr,
        "REGISTER CLIENT (2/3) - ADDRESS",
        [
            ("STREET NAME",   64),
            ("STREET NUMBER", 20),
            ("CITY",          64),
        ],
        "ADD ANOTHER ADDRESS?",
    )
    if not addresses:
        return None

    # Step 3: credit cards (at least one required)
    cards = draw_repeating_form(
        stdscr,
        "REGISTER CLIENT (3/3) - CREDIT CARD",
        [
            ("CARD NUMBER",           19),
            ("BILLING STREET NAME",   64),
            ("BILLING STREET NUMBER", 20),
            ("BILLING CITY",          64),
        ],
        "ADD ANOTHER CARD?",
    )
    if not cards:
        return None

    # Convert to tuples for queries
    addr_tuples = [(a[0], a[1], a[2]) for a in addresses]
    card_tuples = [(c[0], c[1], c[2], c[3]) for c in cards]

    try:
        row = queries.register_client(name, email, addr_tuples, card_tuples)
    except Exception as e:
        stdscr.clear()
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows // 2, 4, f"REGISTRATION FAILED: {e}", "err")
        curses.flushinp()
        stdscr.getch()
        return None

    stdscr.clear()
    rows, _ = stdscr.getmaxyx()
    show_status(stdscr, rows // 2, 4, f"CLIENT {name.upper()} REGISTERED.", "ok")
    curses.flushinp()
    stdscr.getch()
    return row


def client_access(stdscr):
    """Login/register gate before the client console."""
    while True:
        choice = render_client_login_menu(stdscr)

        if choice in QUIT_CMDS:
            return

        if choice == "1":
            result = do_client_login(stdscr)
            if result:
                client_loop(stdscr, result)

        elif choice == "2":
            result = do_client_register(stdscr)
            if result:
                client_loop(stdscr, result)

        else:
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4,
                        "UNKNOWN COMMAND. CONSULT MANUAL.", "err")
            curses.flushinp()
            stdscr.getch()



def manual_action(stdscr):
    render_manual(stdscr)

# Manager actions
def after_action(stdscr, msg, kind="ok"):
    rows, _ = stdscr.getmaxyx()
    show_status(stdscr, rows - 3, 4, msg, kind)
    curses.flushinp()
    stdscr.getch()


def mgr_insert_hotel(stdscr):
    vals = draw_form(stdscr, "INSERT HOTEL", [
        ("HOTEL NAME",    128),
        ("STREET NAME",    64),
        ("STREET NUMBER",  20),
        ("CITY",           64),
    ])
    if not vals:
        return
    try:
        hotel_id = queries.insert_hotel(*vals)
        after_action(stdscr, f"HOTEL CREATED. ID = {hotel_id}", "ok")
    except Exception as e:
        after_action(stdscr, f"INSERT FAILED: {e}", "err")


def mgr_insert_room(stdscr):
    vals = draw_form(stdscr, "INSERT ROOM", [
        ("HOTEL ID",               10),
        ("ROOM NUMBER",            10),
        ("NUM WINDOWS",             5),
        ("LAST RENO YEAR",          4),
        ("ACCESS (elevator/stairs)", 10),
    ])
    if not vals:
        return
    try:
        queries.insert_room(
            int(vals[0]), int(vals[1]),
            int(vals[2]), int(vals[3]),
            vals[4],
        )
        after_action(stdscr, f"ROOM {vals[1]} ADDED TO HOTEL {vals[0]}.", "ok")
    except Exception as e:
        after_action(stdscr, f"INSERT FAILED: {e}", "err")


def mgr_update_hotel(stdscr):
    vals = draw_form(stdscr, "UPDATE HOTEL", [
        ("HOTEL ID",          10),
        ("NEW NAME",         128),
        ("NEW STREET NAME",   64),
        ("NEW STREET NUMBER", 20),
        ("NEW CITY",          64),
    ])
    if not vals:
        return
    try:
        queries.update_hotel(int(vals[0]), vals[1], vals[2], vals[3], vals[4])
        after_action(stdscr, f"HOTEL {vals[0]} UPDATED.", "ok")
    except Exception as e:
        after_action(stdscr, f"UPDATE FAILED: {e}", "err")


def mgr_update_room(stdscr):
    vals = draw_form(stdscr, "UPDATE ROOM", [
        ("HOTEL ID",               10),
        ("ROOM NUMBER",            10),
        ("NUM WINDOWS",             5),
        ("LAST RENO YEAR",          4),
        ("ACCESS (elevator/stairs)", 10),
    ])
    if not vals:
        return
    try:
        queries.update_room(
            int(vals[0]), int(vals[1]),
            int(vals[2]), int(vals[3]),
            vals[4],
        )
        after_action(stdscr, f"ROOM {vals[1]} IN HOTEL {vals[0]} UPDATED.", "ok")
    except Exception as e:
        after_action(stdscr, f"UPDATE FAILED: {e}", "err")


def mgr_remove_hotel(stdscr):
    vals = draw_form(stdscr, "REMOVE HOTEL", [
        ("HOTEL ID", 10),
    ])
    if not vals:
        return
    if not confirm(stdscr, f"CONFIRM REMOVAL OF HOTEL {vals[0]}?"):
        after_action(stdscr, "OPERATION CANCELLED.", "warn")
        return
    try:
        queries.remove_hotel(int(vals[0]))
        after_action(stdscr, f"HOTEL {vals[0]} REMOVED.", "ok")
    except Exception as e:
        after_action(stdscr, f"REMOVE FAILED: {e}", "err")


def mgr_remove_room(stdscr):
    vals = draw_form(stdscr, "REMOVE ROOM", [
        ("HOTEL ID",    10),
        ("ROOM NUMBER", 10),
    ])
    if not vals:
        return
    if not confirm(stdscr, f"CONFIRM REMOVAL OF ROOM {vals[1]} IN HOTEL {vals[0]}?"):
        after_action(stdscr, "OPERATION CANCELLED.", "warn")
        return
    try:
        queries.remove_room(int(vals[0]), int(vals[1]))
        after_action(stdscr, f"ROOM {vals[1]} IN HOTEL {vals[0]} REMOVED.", "ok")
    except Exception as e:
        after_action(stdscr, f"REMOVE FAILED: {e}", "err")


def mgr_remove_client(stdscr):
    vals = draw_form(stdscr, "REMOVE CLIENT", [
        ("CLIENT ID", 10),
    ])
    if not vals:
        return
    if not confirm(stdscr, f"CONFIRM REMOVAL OF CLIENT {vals[0]}?"):
        after_action(stdscr, "OPERATION CANCELLED.", "warn")
        return
    try:
        queries.remove_client(int(vals[0]))
        after_action(stdscr, f"CLIENT {vals[0]} REMOVED.", "ok")
    except Exception as e:
        after_action(stdscr, f"REMOVE FAILED: {e}", "err")


def mgr_top_k_clients(stdscr):
    vals = draw_form(stdscr, "TOP-K CLIENTS BY BOOKINGS", [
        ("K", 5),
    ])
    if not vals:
        return
    try:
        k = int(vals[0])
        if k <= 0:
            raise ValueError("K must be positive")
        results = queries.top_k_clients_by_bookings(k)
    except Exception as e:
        after_action(stdscr, f"QUERY FAILED: {e}", "err")
        return

    render_table(
        stdscr,
        f"TOP-{k} CLIENTS BY BOOKINGS",
        ["NAME", "EMAIL", "BOOKINGS"],
        results,
    )

def mgr_list_hotels(stdscr):
    try:
        results = queries.list_hotels()
    except Exception as e:
        after_action(stdscr, f"QUERY FAILED: {e}", "err")
        return
    render_table(
        stdscr,
        "HOTELS",
        ["ID", "NAME", "STREET", "NUMBER", "CITY"],
        results,
    )


def mgr_list_rooms(stdscr):
    vals = draw_form(stdscr, "LIST ROOMS (BLANK = ALL)", [
        ("HOTEL ID (OPTIONAL)", 10),
    ])
    if vals is None:
        return
    hotel_id = None
    if vals[0]:
        try:
            hotel_id = int(vals[0])
        except ValueError:
            after_action(stdscr, "HOTEL ID MUST BE A NUMBER.", "err")
            return
    try:
        results = queries.list_rooms(hotel_id)
    except Exception as e:
        after_action(stdscr, f"QUERY FAILED: {e}", "err")
        return
    render_table(
        stdscr,
        "ROOMS" + (f" (HOTEL {hotel_id})" if hotel_id else ""),
        ["HOTEL ID", "HOTEL", "ROOM", "WINDOWS", "RENO", "ACCESS"],
        results,
    )


def mgr_list_clients(stdscr):
    try:
        results = queries.list_clients()
    except Exception as e:
        after_action(stdscr, f"QUERY FAILED: {e}", "err")
        return
    render_table(
        stdscr,
        "CLIENTS",
        ["ID", "NAME", "EMAIL"],
        results,
    )

# Loops for each user and their actions
MANAGER_ACTIONS = {
    "1":  mgr_list_hotels,
    "2":  mgr_list_rooms,
    "3":  mgr_list_clients,
    "4":  mgr_insert_hotel,
    "5":  mgr_insert_room,
    "6":  mgr_update_hotel,
    "7":  mgr_update_room,
    "8":  mgr_remove_hotel,
    "9":  mgr_remove_room,
    "10": mgr_remove_client,
    "11": mgr_top_k_clients,
}

def manager_loop(stdscr, manager_row):
    """manager_row = (ssn, name, email)"""
    while True:
        choice = render_manager_menu(stdscr, manager_row[1])
        if choice in QUIT_CMDS:
            return
        action = MANAGER_ACTIONS.get(choice)
        if action is None:
            rows, _ = stdscr.getmaxyx()
            show_status(stdscr, rows - 3, 4,
                        "NOT YET IMPLEMENTED.", "warn")
            curses.flushinp()
            stdscr.getch()
            continue
        action(stdscr)


def client_loop(stdscr, client_row):
    while True:
        choice = render_client_menu(stdscr, client_row[1])
        if choice in QUIT_CMDS:
            return
        rows, _ = stdscr.getmaxyx()
        show_status(stdscr, rows - 3, 4, "TODO", "warn")
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
        choice = render_main_menu(stdscr)

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
            show_status(stdscr, rows - 3, 4, "UNKNOWN COMMAND. CONSULT MANUAL.", "err")
            curses.flushinp()
            stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)