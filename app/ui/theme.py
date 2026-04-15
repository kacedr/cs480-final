# Visual constants: color pair IDs, box drawing characters, banner text.
# Anything to tweek the look is in here

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