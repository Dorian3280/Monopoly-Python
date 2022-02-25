import curses
import numpy as np
from constants import TITLES
from sentences import *
from cases import *

std = curses.initscr()

curses.start_color()
curses.use_default_colors()
curses.init_pair(1, 131, -1) # Brown
curses.init_pair(2, 51, -1) # Light Blue
curses.init_pair(3, 206, -1) # Pink
curses.init_pair(4, 208, -1) # Orange
curses.init_pair(5, 4, -1) # Red
curses.init_pair(6, 14, -1) # Yellow
curses.init_pair(7, 2, -1) # Green
curses.init_pair(8, 27, -1) # Dark Blue
curses.init_pair(9, 244, -1) # Light Grey
curses.init_pair(10, 1, -1) # White


class Displayer:
    def __init__(self):

        self.actions = self.displayElement(12, 40, 2, 1)  # actionsDisplay
        self.history = self.displayElement(12, 60, 2, 45)  # historyDisplay
        self.gameInfo = self.displayElement(12, 40, 2, 110)  # InfoDisplay
        self.text = self.displayElement(4, 149, 15, 1)  # textDisplay
        self.write(std, 1, 6, TITLES["action"])
        self.write(std, 1, 68, TITLES["history"])
        self.write(std, 1, 118, TITLES["gameInfo"])
        self.write(std, 14, 64, TITLES["text"])
        self.write(std, 20, 100, TITLES["player"])

    def __call__(self):
        self.refreshElement(self.actions)
        self.refreshElement(self.history)
        self.refreshElement(self.text)
        self.refreshElement(self.gameInfo)
        return self.actions, self.history, self.text, self.gameInfo

    def displayElement(self, h, w, y, x):
        element = curses.newwin(h, w, y, x)
        element.border()
        return element

    def propertiesOfPlayer(self, id):
        case = cases[id]
        built = ''
        mortgaged = mortgage if case['mortgaged'] else ''
        if case['type'] == 'property':
            built = '' if not case['built'] else (case['built'] + ' ' + house + ('s' if case['built'] > 1 else '') if case['built'] < 5 else '1 ' + hotel)
        
        state = f"{mortgaged} {built}"
        return f" {' ->' if state != ' ' else ''} {state}"

    def player(self, player):
        w = 55
        x = 1 + player.id*w
        pos = cases[player.location]['name'] if not player.inJail else cases[player.location]['namebis']
        win = self.displayElement(25, w, 22, x)
        self.write(win, 1, 2, f"{namePlayer(player.id):^50s}")
        self.write(win, 2, 2, f"{money} : {player.money} €")
        self.write(win, 3, 2, f"{location} : {pos}", color=cases[player.location]["idColor"])
        self.write(win, 5, 2, f"{owning:^50s}")

        casesID = np.nonzero(player.own[:, :, 0])

        for i, (familyID, caseID) in enumerate(zip(*casesID)):
            id = model[familyID][caseID]
            self.write(win, 7+i, 2, f"{cases[id]['name']}{self.propertiesOfPlayer(id)}", color=cases[id]["idColor"])

    def write(self, component, y, x, text, color=8):
        component.addstr(y, x, text, curses.color_pair(color+1))
        component.refresh()
    
    def refreshElement(self, element):
        element.clear()
        element.border()
        element.refresh()

    def refreshElements(self, *elements):
        for element in elements:
            element.clear()
            element.border()
            element.refresh()
