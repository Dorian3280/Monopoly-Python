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
def display():
    write(std, 0, 4, TITLES['action'])
    write(std, 0, 57, TITLES['history'])
    write(std, 0, 103, TITLES['choice'])
    write(std, 0, 157, TITLES['player'])
    write(std, 14, 85, TITLES['text'])
    return displayElement(12, 30, 1, 0), displayElement(12, 60, 1, 33), displayElement(4, 190, 15, 0), displayElement(12, 40, 1, 95)

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

def loopWrite(component, y, x, texts, color=COLORS[9]):
    for i in range(len(texts)):
        write(component, y+i, x, f"{i+1}: {texts[i]}", color)

def rollDice():
    pass

def end():
    std.getch()
    quit()