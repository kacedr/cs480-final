# Visual constants: color pair IDs, box drawing characters, banner text.
# Anything to tweek the look is in here

# ctrl-c also works lmao
QUIT_CMDS = {"0", ":q", "quit", "exit"}

ERROR_UNKNOWN_COMMAND = "UNKNOWN COMMAND. CONSULT MANUAL. PRESS ANY KEY TO RETURN"

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
    ("2", "MANAGER LOGIN/REGISTER",   PAIR_TITLE),
    ("3", "CLIENT LOGIN/REGISTER",    PAIR_TITLE),
    ("4", "MANUAL",                   PAIR_TITLE),
    ("0", "DISCONNECT",               PAIR_ERR),
]

MANAGER_LOGIN_ITEMS = [
    ("1", "LOGIN WITH SSN",      PAIR_TITLE),
    ("2", "REGISTER NEW MANAGER", PAIR_TITLE),
    ("0", "BACK",                 PAIR_ERR),
]

CLIENT_LOGIN_ITEMS = [
    ("1", "LOGIN WITH EMAIL",     PAIR_TITLE),
    ("2", "REGISTER NEW CLIENT",  PAIR_TITLE),
    ("0", "BACK",                 PAIR_ERR),
]

MANAGER_MENU_ITEMS = [
    ("1",  "LIST HOTELS",               PAIR_INFO),
    ("2",  "LIST ROOMS",                PAIR_INFO),
    ("3",  "LIST CLIENTS",              PAIR_INFO),
    ("4",  "INSERT HOTEL",              PAIR_TITLE),
    ("5",  "INSERT ROOM",               PAIR_TITLE),
    ("6",  "UPDATE HOTEL",              PAIR_TITLE),
    ("7",  "UPDATE ROOM",               PAIR_TITLE),
    ("8",  "REMOVE HOTEL",              PAIR_TITLE),
    ("9",  "REMOVE ROOM",               PAIR_TITLE),
    ("10", "REMOVE CLIENT",             PAIR_TITLE),
    ("11", "TOP-K CLIENTS BY BOOKINGS", PAIR_TITLE),
    ("12", "ROOM BOOKING COUNTS",       PAIR_TITLE),
    ("13", "HOTEL STATISTICS",          PAIR_TITLE),
    ("14", "CLIENTS BY CITY PAIR",      PAIR_TITLE),
    ("15", "PROBLEMATIC HOTELS",        PAIR_TITLE),
    ("16", "CLIENT SPENDING REPORT",    PAIR_TITLE),
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