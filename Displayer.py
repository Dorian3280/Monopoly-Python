import curses
import numpy as np
from constants import TITLES, COLORS
from sentences import *
from cases import *

std = curses.initscr()


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
        state = mortgage if case['mortgaged'] else '' + '' + '' if not case['built'] else (case['built'] + ' ' + house + ('s' if case['built'] > 1 else '') if case['built'] < 5 else '1 ' + hotel)
        return f" {' -> ' if state != '' else ''} {state}"

    def player(self, player):
        y = 2 + player.id*55
        pos = cases[player.location]['name'] if not player.inJail else cases[player.location]['namebis']
        win = self.displayElement(25, 55, 22, 1 + y)
        self.write(win, 1, 2, f"{namePlayer(player.id):^50s}")
        self.write(win, 2, 2, f"{money} : {player.money} €")
        self.write(win, 3, 2, f"{location} : {pos}", color=COLORS[cases[player.location]["idColor"]])
        self.write(win, 5, 2, f"{owning:^50s}")
        casesID = np.nonzero(player.own[:, :, 0])
        for i, (familyID, caseID) in enumerate(zip(*casesID)):
            id = model[familyID][caseID]
            self.write(win, 7+i, y, f"{cases[id]['name']}{self.propertiesOfPlayer(id)}", color=COLORS[cases[player.location]["idColor"]])

    def write(self, component, y, x, text, color=COLORS[8]):
        component.addstr(y, x, text, color)
        component.refresh()

    def loopWrite(self, component, y, x, indices, texts, color=COLORS[8]):
        for i in range(len(texts)):
            self.write(component, y + i, x, f"{indices[i]} : {texts[i]}", color)

    def refreshElement(self, element):
        element.clear()
        element.border()
        element.refresh()

    def refreshElements(self, *elements):
        for element in elements:
            element.clear()
            element.border()
            element.refresh()
