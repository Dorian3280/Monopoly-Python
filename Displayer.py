import curses
from genericpath import isfile
import numpy as np
from constants import TITLES
from sentences import *
from cases import *

std = curses.initscr()

curses.start_color()
curses.use_default_colors()


class Displayer:
    def __init__(self):

        self.actions = self.displayElement(12, 40, 2, 1)  # actionsDisplay
        self.history = self.displayElement(12, 60, 2, 45)  # historyDisplay
        self.transaction = self.displayElement(12, 12, 2, 104)  # transactionDisplay
        self.info = self.displayElement(12, 30, 2, 120)  # InfoDisplay
        self.text = self.displayElement(4, 149, 16, 1)  # textDisplay
        self.write(std, 1, 6, text=TITLES["action"])
        self.write(std, 1, 75, text=TITLES["history"])
        self.write(std, 1, 123, text=TITLES["info"])
        self.write(std, 15, 64, text=TITLES["text"])
        self.write(std, 21, 100, text=TITLES["player"])

        self.historyCount = 0

    def __call__(self):
        self.refreshElement(self.actions)
        self.refreshElement(self.history)
        self.refreshElement(self.transaction)
        self.refreshElement(self.info)
        self.refreshElement(self.text)
        return self.actions, self.history, self.transaction, self.info, self.text

    @staticmethod
    def initColor():
        curses.init_pair(1, 131, -1)  # Brown
        curses.init_pair(2, 51, -1)  # Light Blue
        curses.init_pair(3, 206, -1)  # Pink
        curses.init_pair(4, 208, -1)  # Orange
        curses.init_pair(5, 4, -1)  # Red
        curses.init_pair(6, 228, -1)  # Yellow
        curses.init_pair(7, 2, -1)  # Green
        curses.init_pair(8, 27, -1)  # Dark Blue
        curses.init_pair(9, 253, -1)  # Light Grey
        curses.init_pair(10, -1, -1)  # White

    def displayElement(self, h, w, y, x):
        element = curses.newwin(h, w, y, x)
        element.border()
        return element

    def propertiesOfPlayer(self, id, isFamily):
        case = cases[id]
        built = ""
        mortgaged = mortgage if case["mortgaged"] else ""
        if case["type"] == "property":
            built = (
                ""
                if not case["built"]
                else (
                    f"{case['built']} {house}{'s' if case['built'] > 1 else ''}"
                    if case["built"] < 5
                    else f"{hotel.title()}"
                )
            )
        state = f"{mortgaged}{built}"

        return f" {'|' if state != '' else ('<>' if isFamily else '')} {state}"

    def player(self, player):
        w = 55
        x = 1 + player.id * w
        pos = (
            cases[player.location]["name"]
            if not player.inJail
            else cases[player.location]["namebis"]
        )
        win = self.displayElement(25, w, 23, x)

        if player.bankruptcy:
            self.write(win, 9, 1, text=f"{namePlayer(player.id):^50s}", color=5)
            self.write(win, 11, 1, text=f"{bankruptcy:^50s}", color=5)
        else:

            self.write(win, 1, 2, text=f"{namePlayer(player.id):^50s}")
            self.write(win, 2, 2, text=f"{money} : {player.money} €")
            self.write(
                win,
                3,
                2,
                text=f"{location} : {pos}",
                color=cases[player.location]["idColor"],
            )
            self.write(win, 5, 2, text=f"{owning:^50s}")

            casesID = np.nonzero(player.own[:, :, 0])

            for i, (familyID, caseID) in enumerate(zip(*casesID)):
                id = model[familyID][caseID]
                self.write(
                    win,
                    7 + i,
                    2,
                    text=f"{cases[id]['name']}{self.propertiesOfPlayer(id, player.isFamily(id))}",
                    color=cases[id]["idColor"],
                )

    def write(self, component, y=1, x=2, text="", color=10):
        if component == self.history:
            if self.historyCount > 9:
                self.historyCount = 1
                self.refreshElement(self.history)
                self.refreshElement(self.transaction)

            else:
                self.historyCount += 1

            y = self.historyCount

        if component == self.transaction:
            y = self.historyCount

        component.addstr(y, x, text, curses.color_pair(color))
        component.refresh()

    def refreshHistoryCount(self):
        self.historyCount = 0

    def refreshElement(self, element):
        element.clear()
        element.border()
        element.refresh()

    def refreshElements(self, *elements):
        for element in elements:
            element.clear()
            element.border()
            element.refresh()
