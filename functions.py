import curses
import time

from sentences import *
from classes import *


stdscr = curses.initscr()


def ask(typeof, test):
    while True:
        res = stdscr.getkey()
        try:
            res = typeof(res)
            if not test(res):
                raise Exception
            return res
        except ValueError and Exception:
            pass


def initializePlayers(nbr):
    return [Player(i, f"{player} {i}") for i in range(nbr)]
