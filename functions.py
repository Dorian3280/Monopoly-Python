import curses
import time

from numpy import random
from sentences import *
from constants import COLORS


std = curses.initscr()


def ask(typeof, test):
    while True:
        res = std.getkey()
        try:
            res = typeof(res)
            if not test(res):
                raise Exception
            return res
        except ValueError and Exception:
            pass

def displayElement(h, w, y, x):
    element = curses.newwin(h, w, y, x)
    element.border()
    element.refresh()
    return element

def refreshElement(element):
    element.clear()
    element.border()
    element.refresh()

def refreshElements(*elements):
    for element in elements:
        element.clear()
        element.border()
        element.refresh()



def write(component, y, x, text, color=COLORS[9]):
    component.addstr(y, x, text, color)
    component.refresh()

def rollDice():
    pass

def end():
    std.getch()
    quit()