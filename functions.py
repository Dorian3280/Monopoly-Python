import curses
import time

from numpy import random
from sentences import *
from constants import COLORS, TITLES


std = curses.initscr()

def end():
    std.getch()
    quit()