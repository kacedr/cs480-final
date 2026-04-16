# Visual constants: color pair IDs, box drawing characters, banner text.
# Anything to tweek the look is in here

# ctrl-c also works lmao
QUIT_CMDS = {"0", ":q", "quit", "exit"}

# Color pair IDs (defined in primitives.init_colors)
PAIR_DEFAULT = 1
PAIR_BORDER  = 2   # cyan border
PAIR_TITLE   = 3   # yellow title
PAIR_OK      = 4   # green
PAIR_ERR     = 5   # red
PAIR_WARN    = 6   # yellow
PAIR_INFO    = 7   # cyan
PAIR_DIM     = 8   # dim white

# Box drawing characters
TL, TR, BL, BR = "╔", "╗", "╚", "╝"
H, V           = "═", "║"
LT, RT         = "╠", "╣"

# Splash text
BANNER = r"""
   ____ ____    _  _    ___ ___
  / ___/ ___|  | || |  ( _ ) _ \
 | |   \___ \  | || |_ / _ \ | | |
 | |___ ___) | |__   _| (_) |_| |
  \____|____/     |_|  \___/\___/
""".strip("\n").splitlines()

SUBTITLE  = "H O T E L   R E S E R V A T I O N   S Y S T E M"
COPYRIGHT = "(C) 2026 GLEASON / GROSCH / NGUYEN / PATEL  -  ALL RIGHTS RESERVED"
TERMINAL  = "TERMINAL READY  -  VT220 EMULATION  -  9600 BAUD"

# Menu definitions
MAIN_MENU_ITEMS = [
    ("1", "TEST DATABASE CONNECTION", PAIR_TITLE),
    ("2", "MANAGER LOGIN",            PAIR_TITLE),
    ("3", "CLIENT LOGIN",             PAIR_TITLE),
    ("4", "HELP",                     PAIR_TITLE),
    ("0", "DISCONNECT",               PAIR_ERR),
]

MANAGER_MENU_ITEMS = [
    ("1",  "INSERT HOTEL",              PAIR_TITLE),
    ("2",  "INSERT ROOM",               PAIR_TITLE),
    ("3",  "UPDATE HOTEL",              PAIR_TITLE),
    ("4",  "UPDATE ROOM",               PAIR_TITLE),
    ("5",  "REMOVE HOTEL",              PAIR_TITLE),
    ("6",  "REMOVE ROOM",               PAIR_TITLE),
    ("7",  "REMOVE CLIENT",             PAIR_TITLE),
    ("8",  "TOP-K CLIENTS BY BOOKINGS", PAIR_TITLE),
    ("9",  "ROOM BOOKING COUNTS",       PAIR_TITLE),
    ("10", "HOTEL STATISTICS",          PAIR_TITLE),
    ("11", "CLIENTS BY CITY PAIR",      PAIR_TITLE),
    ("12", "PROBLEMATIC HOTELS",        PAIR_TITLE),
    ("13", "CLIENT SPENDING REPORT",    PAIR_TITLE),
    ("0",  "LOGOUT",                    PAIR_ERR),
]

CLIENT_MENU_ITEMS = [
    ("1", "UPDATE MY NAME",         PAIR_TITLE),
    ("2", "MANAGE ADDRESSES",       PAIR_TITLE),
    ("3", "MANAGE CREDIT CARDS",    PAIR_TITLE),
    ("4", "SEARCH AVAILABLE ROOMS", PAIR_TITLE),
    ("5", "BOOK A ROOM",           PAIR_TITLE),
    ("6", "AUTO-BOOK",             PAIR_TITLE),
    ("7", "VIEW MY BOOKINGS",      PAIR_TITLE),
    ("8", "WRITE A REVIEW",        PAIR_TITLE),
    ("0", "LOGOUT",                PAIR_ERR),
]