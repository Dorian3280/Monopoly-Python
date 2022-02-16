import curses
import numpy as np

from cases import cases
from functions import *
from sentences import *
from constants import COLORS

stdscr = curses.initscr()
resolution = curses.LINES, curses.COLS
model = [
    len(i["membership"])
    for i in sorted(
        cases, key=lambda x: x["idProperty"] if "idProperty" in x.keys() else np.Inf
    )
    if "idProperty" in i.keys() and i["membership"][0] == i["idProperty"]
]


class Player:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.__money = 1500
        self.__location = 0
        self.own = np.zeros((10, 4, 3))
        self.double = False
        self.countDouble = 0
        self.dices = None
        self.turn = True
        self.__historyCount = 1
        self.displayPlayer()

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, x):
        self.__money = x
        self.displayPlayer()

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, x):
        self.__location = x
        self.displayPlayer()

    @property
    def historyCount(self):
        temp = self.__historyCount
        self.__historyCount += 1
        return temp
    
    def displayPlayer(self):
        win = displayElement(4, 50, 1 + self.id * 4, 140)
        write(win, 1, 1, f"Joueur {self.id} : {self.money} €")
        write(
            win,
            2,
            1,
            f"{cases[self.location]['name']}",
            COLORS[cases[self.location]["idColor"]],
        )

    def payTo(self, player, amount):
        self.money = self.money - amount
        player.money = player.money + amount

    def transaction(self, amount):
        self.money = self.money + amount

    def hasFamily(self):
        return any(
            all(self.own[z, :i, 0])
            and all(self.own[z, :i, 1] == 0)
            and all(self.own[z, :i, 1] == 0)
            and all(self.own[z, :i, 1] == 5)
            for i, z in zip(model, range(10))
        )

    def isFamily(self, case):
        idFamily = case['idFamily']
        return all(self.own[idFamily, : model[idFamily], 0]) and all(
            self.own[idFamily, : model[idFamily], 1] == 0
        )

    def isBuilt(self, case):
        return self.own[
            case["idFamily"], case["membership"].index(case["idProperty"]), 2
        ]

    def getPrice(self, case):
        isFamily = self.isFamily(case)
        if case['type'] == 'property':
            if isFamily:
                built = self.isBuilt(case["id"])
                if built == 5:
                    return case["hotel"]
                elif built:
                    return case[f"house_{built}"]
                else:
                    return case["rent"] * 2
            return case["rent"]
        elif case['type'] == 'station':
            return case['rent'] * np.count_nonzero(self.own[case['idFamily'], :, 0])
        else:
            return 4 * np.sum(self.dices) if not isFamily else 10 * np.sum(self.dices)

    def endTurn(self):
        self.__historyCount = 1
        self.turn = True

    def checkActions(self):
        # Roll dice
        if self.turn:
            yield 0
        # Mortgage
        if np.any(self.own[:, :, 0]) and np.any(
            self.own[~np.all(self.own == 0, axis=2)][:, 1] == 0
        ):
            yield 1
        # Unmortgage
        if np.any(self.own[:, :, 0]) and np.any(
            self.own[~np.all(self.own == 0, axis=2)][:, 1]
        ):
            yield 2
        # Build
        if self.hasFamily():
            yield 3
        # Sell
        if np.any(self.own[:, :, 2]):
            yield 4
        # End turn
        if not self.turn:
            yield 5
            