import curses
import numpy as np

from Tiles import *
from constants import LANG
from sentences import *

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
        self.write(std, 1, 10, text=TITLES["action"][LANG])
        self.write(std, 1, 75, text=TITLES["history"][LANG])
        self.write(std, 1, 123, text=TITLES["info"][LANG])
        self.write(std, 15, 64, text=TITLES["text"][LANG])
        self.write(std, 21, 100, text=TITLES["player"][LANG])

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

    @staticmethod
    def formatName(name: str, visiting=None):
        if visiting is not None:
            return (
                name.split("|")[0 if visiting else 1]
                .split(",")[LANG]
                .replace("_", " ")
                .title()
            )
        return name.split(",")[LANG].replace("_", " ").title()

    def displayElement(self, h, w, y, x):
        element = curses.newwin(h, w, y, x)
        element.border()
        return element

    def propertiesOfPlayer(self, case):
        caseState = getState(case)
        built = ""
        mortgaged = mortgage[LANG] if caseState["mortgaged"] else ""
        
        if case["type"] == "property":
            built = (
                ""
                if not caseState["built"]
                else (
                    f"{caseState['built']} {house}{'s' if caseState['built'] > 1 else ''}"
                    if caseState["built"] < 5
                    else f"{hotel.title()}"
                )
            )
        state = f"{mortgaged}{built}"

        return f" {'|' if state != '' else ('<>' if caseState['isFamily'] else '')} {state}"

    def player(self, player):
        w = 55
        x = 1 + player.id * w

        pos = (
            self.formatName(TILES.loc[player.location]["name"])
            if not player.location == 10
            else self.formatName(
                TILES.loc[player.location]["name"], visiting=(not player.inJail)
            )
        )
        win = self.displayElement(25, w, 23, x)

        if player.bankruptcy:
            self.write(win, 9, 1, text=f"{player.name:^50s}", color=5)
            self.write(win, 11, 1, text=f"{bankruptcy[LANG]:^50s}", color=5)
        else:

            self.write(win, 1, 2, text=f"{player.name:^50s}")
            self.write(win, 2, 2, text=f"{money[LANG]} : {player.money} €")
            self.write(
                win,
                3,
                2,
                text=f"{location[LANG]} : {pos}",
                color=TILES.loc[player.location]["idColor"],
            )
            self.write(win, 5, 2, text=f"{owning[LANG]:^50s}")

            indexes = np.where(states[:, :, 0] == player.id)

            for i, (familyID, caseID) in enumerate(zip(*indexes)):
                case = TILES.loc[SETS[familyID][caseID]]
                self.write(
                    win,
                    7 + i,
                    2,
                    text=f"{self.formatName(case['name'])}{self.propertiesOfPlayer(case)}",
                    color=case["idColor"],
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
