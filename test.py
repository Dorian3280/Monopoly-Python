import curses
from curses import textpad
from re import S

stdscr = curses.initscr()

import config
import test2
import numpy as np
from sentences import ACTIONS

arrayActions = [0, 2, 5]
print("".join(map(str, arrayActions)))
