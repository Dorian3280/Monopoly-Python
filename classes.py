import curses
import numpy as np

from cases import cases
from sentences import *
from constants import colors

stdscr = curses.initscr()
resolution = curses.LINES, curses.COLS
model = (
    len(i["membership"])
    for i in sorted(
        cases, key=lambda x: x["idProperty"] if "idProperty" in x.keys() else np.Inf
    )
    if "idProperty" in i.keys() and i["membership"][0] == i["idProperty"]
)


class Player:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.__money = 1500
        self.__location = 0
        self.own = np.zeros((10, 4, 3))
        self.double = (False, 0)
        self.endTurn = False
        self.displayPlayer()

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, x):
        bool = self.__money > x
        amount = abs(self.__money - x)
        self.__money = x
        self.displayPlayer()
        print(
            f"""Le joueur {self.id} a {"perdu" if bool else "gagné"} {amount} et a maintenant {self.__money} €."""
        )

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, x):
        self.__location = x
        self.displayPlayer()

    def displayPlayer(self):
        win = curses.newwin(4, 20, 1 + self.id * 4, 90)
        win.border()
        win.addstr(1, 1, f"Joueur {self.id} : {self.money} €")
        win.addstr(
            2,
            1,
            f"{cases[self.location]['name']}",
            colors[cases[self.location]["idColor"]],
        )
        win.refresh()

    def hasFamily(self):
        return any(
            all(self.own[z, :i, 0])
            and all(self.own[z, :i, 1] == 0)
            and all(self.own[z, :i, 1] == 0)
            and all(self.own[z, :i, 1] == 5)
            for i, z in zip(model, range(10))
        )

    def isFamily(self, id):
        idFamily = cases[id]["idFamily"]
        return all(self.own[idFamily, : model[idFamily], 0]) and all(
            self.own[idFamily, : model[idFamily], 1] == 0
        )

    def checkActions(self):
        # Roll dice
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
        if self.endTurn:
            yield 5
