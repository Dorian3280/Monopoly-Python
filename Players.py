import curses
import numpy as np

from cases import *
from functions import *
from sentences import *
from constants import COLORS

stdscr = curses.initscr()

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
        self.forced = False
        self.inJail = False
        self.countTurn = 0
        self.__historyCount = 1
        self.free = 0
        self.bankruptcy = False
        self.displayPlayer()
    
    def getFreeCard(self):
        self.free += 1
        
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

    def isFamily(self, case):
        idFamily = model.index(case['membership'])
        return bool(np.where((np.count_nonzero(self.own[idFamily, :len(model[idFamily]), 0] == 1) == len(model[idFamily])) & (self.own[idFamily, :len(model[idFamily]), 1] == 0))[0].size)

    def isBuilt(self, case):
        return self.own[
            model.index(case['membership']), case["membership"].index(case["id"]), 2
        ]

    def moveByDice(self, nbr):
        self.location = self.location + nbr
        if self.location > 40:
            self.transaction(200)
            self.location -= 40
    
    def moveByCard(self, where, backward=False, moveBackward=False):
        self.forced = True

        if self.location > where and not backward and not moveBackward:
            self.transaction(200)

        self.location = where if not moveBackward else self.location + where

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
        self.move(10, forced=True, jail=True)

    def endTurn(self):
        self.move = False
        self.__historyCount = 1
        self.turn = True

    def mortgage(self, case):
        case['mortgaged'] = True
        self.own[model.index(case['membership']), case['membership'].index(case['id']), 1] = 1
        self.transaction(case['mortgagePrice'])

    def unmortgage(self, case):
        case['mortgaged'] = False
        self.own[model.index(case['membership']), case['membership'].index(case['id']), 1] = 0
        self.transaction(-case['mortgagePrice'])

    def build(self, case):
        self.own[model.index(case['membership']), case['membership'].index(case['id']), 1] += 1
        self.transaction(-case['housePrice'])

    def sell(self, case):
        self.own[model.index(case['membership']), case['membership'].index(case['id']), 1] -= 1
        self.transaction(case['housePrice']/2)

    def getIdOfMortgageable(self):
        indexes = np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 0))
        return [model[i][y] for i, y in zip(*indexes)]

    def getIdOfUnmortgageable(self):
        indexes = np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 1))
        return [model[i][y] for i, y in zip(*indexes)]

    def mortgageable(self):
        return bool(np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 0))[0])

    def unmortgageable(self):
        return bool(np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 1))[0])

    def getIdOfBuildable(self):
        res = []
        for z in range(len(model)):
            if z != 0 or z != 9:
                indexes = np.where((np.count_nonzero(self.own[z, :len(model[z]), 0] == 1) == len(model[z])) & (self.own[z, :len(model[z]), 1] == 0) & (np.amin(self.own[z, :len(model[z]), 2]) >= self.own[z, :len(model[z]), 2]) & (self.own[z, :len(model[z]), 2] <= 5))[0]
                for i in indexes:
                    res.append(model[z][i]) 
        return res
    
    def getIdOfSaleable(self):
        res = []
        for z in range(len(model)):
            if z != 0 or z != 9:
                indexes = np.where((self.own[z, :len(model[z]), 2] > 0) & (np.amax(self.own[z, :len(model[z]), 2]) <= self.own[z, :len(model[z]), 2]))[0]
                for i in indexes:
                    res.append(model[z][i]) 
        return res

    def checkActions(self):
        # Roll dice
        if self.turn:
            yield 0
        # Mortgage
        if self.mortgageable():
            yield 1
        # Unmortgage
        if self.unmortgageable():
            yield 2
        # Build
        if bool(self.getIdOfBuildable()):
            yield 3
        # Sell
        if bool(self.getIdOfSaleable()):
            yield 4
        # End turn
        if not self.turn or self.money < 0:
            yield 5
        # Quit
        if True:
            yield 6
        if self.free:
            yield 7

    def getPriceOfAllBuildingsForTHEFUCKING_Card(self):
        return self.own[self.own[:, :, 2] < 5][:, 2].sum() * 25 + np.count_nonzero(self.own[:, :, 2] == 5) * 100

    def getPriceOfAllBuildingsForTHEWORSTFUCKING_Card(self):
        return self.own[self.own[:, :, 2] < 5][:, 2].sum() * 40 + np.count_nonzero(self.own[:, :, 2] == 5) * 115
    # Sorry.... I has to