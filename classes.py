import curses
import numpy as np

from cases import *
from functions import *
from sentences import *
from constants import COLORS

stdscr = curses.initscr()
resolution = curses.LINES, curses.COLS

class Player:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.__money = 1500
        self.__location = 0
        self.own = np.zeros((10, 4, 3), dtype=int)
        self.double = False
        self.countDouble = 0
        self.dices = None
        self.turn = True
        self.extraMove = False
        self.inJail = False
        self.countTurn = 0
        self.__historyCount = 1
        self.free = 0
        self.displayPlayer()
    
    def getFreeCard(self):
        self.free += 1
    def move(self, x):
        self.move = x
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
        if x < 40: self.displayPlayer()

    @property
    def historyCount(self):
        temp = self.__historyCount
        self.__historyCount += 1
        return temp
    
    def displayPlayer(self):
        win = displayElement(4, 40, 1 + self.id * 4, 150)
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
            all(self.own[z, :len(i), 0])
            and all(self.own[z, :len(i), 1] == 0)
            and all(self.own[z, :len(i), 1] == 0)
            and all(self.own[z, :len(i), 1] == 5)
            for i, z in zip(model, range(10))
        )
    def move(self, nbr, teleportation, backward=False, jail=False):
        
        if teleportation == False:
            self.location = self.location + nbr
            if self.location > 40:
                self.transaction(200)
                self.location -= 40
            elif self.location < 0:
                self.location = 40 + self.location
        else:
            if jail:
                self.inJail = True
            elif self.location > nbr and not backward:
                self.transaction(200)
            self.location = nbr

    def isFamily(self, case):
        idFamily = model.index(case['membership'])
        return all(self.own[idFamily, : len(model[idFamily]), 0]) and all(
            self.own[idFamily, : len(model[idFamily]), 1] == 0
        )

    def isBuilt(self, case):
        return self.own[
            model.index(case['membership']), case["membership"].index(case["id"]), 2
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
            return case['rent'] * np.count_nonzero(self.own[model.index(case['membership']), :, 0])
        else:
            return 4 * np.sum(self.dices) if not isFamily else 10 * np.sum(self.dices)

    def goToJail(self):
        self.turn = False
        self.inJail = True
        self.move(10, True, jail=True)
        
    def endTurn(self):
        self.move = False
        self.__historyCount = 1
        self.turn = True

    def mortgage(self, case):
        case['mortgaged'] = True
        self.own[model.index(case['membership']), case['membership'].index(case['id']), 1] = 1
        self.transaction(case['mortgagePrice'])

    def unMortgage(self, case):
        case['mortgaged'] = False
        self.own[model.index(case['membership']), case['membership'].index(case['id']), 1] = 0
        self.transaction(-case['mortgagePrice'])

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
        # Quit
        if True:
            yield 6
        if self.free:
            yield 7

    def countConstruction(self):
        return self.own[self.own[:, :, 2] < 5][:, 2].sum(), np.count_nonzero(self.own[:, :, 2] == 5)