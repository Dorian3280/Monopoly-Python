import curses
import numpy as np

from cases import *
from sentences import *
from constants import *
from Displayer import Displayer

std = curses.initscr()

displayer = Displayer()
actionsDisplay, historyDisplay, textDisplay = displayer()


class Player:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.__money = 1500
        self.__location = 0
        self.own = np.zeros((10, 4, 3), dtype=int)
        self.action = False
        self.double = False
        self.tryDouble = False
        self.countDouble = 0
        self.totalDices = 0
        self.loopWhile = False
        self.actions = []
        self.turn = True
        self.response = 0
        self.inJail = False
        self.forcedToJail = False
        self.moveOutOfJail = False
        self.countTurnInJail = 0
        self.__historyCount = 1
        self.freeJailCard = 0
        self.bankruptcy = False
        displayer.player(self)

    def __call__(self):
        displayer.write(historyDisplay, self.historyCount, 1, f"{tour(self.name)}")

    def __str__(self) -> str:
        return f"id : {self.id}\nturn : {self.turn}\nforcedToJail : {self.forcedToJail}\ninJail : {self.inJail}\ndouble : {self.double}\nmoveOutOfJail : {self.moveOutOfJail}\ncountTurnInJail : {self.countTurnInJail}\ntryDouble : {self.tryDouble}"

    def getFreeJailCard(self):
        self.freeJailCard += 1

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, x):
        self.__money = x
        displayer.player(self)

    @property
    def response(self):
        return self.__money

    @response.setter
    def response(self, x):
        displayer.refreshElement(actionsDisplay)

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, x):
        self.__location = x
        if x < 40:
            displayer.player(self)

    @property
    def historyCount(self):
        temp = self.__historyCount
        self.__historyCount += 1
        return temp

    def choice(self, nbr, texts, multiple=False):
        displayer.refreshElement(actionsDisplay)
        displayer.loopWrite(actionsDisplay, 1, 1, nbr, texts)
        while True:
            curses.flushinp()
            try:
                x = std.getkey() if multiple else "0"
                y = std.getkey()
                if y == 'q':
                    quit()
                if y == 'c':
                    return False
                res = int(x + y)
                if res not in nbr:
                    raise Exception
                return res
            except ValueError and Exception:
                pass

    def rollDice(self):
        dices = np.random.randint(1, 7, size=2)
        self.totalDices = np.sum(dices)
        self.totalDices = 7
        if dices[0] == dices[1]:
            self.countDouble += 1
            self.double = True

            if self.countDouble == 3:
                self.moveToJail()

        else:
            self.double = False
            self.turn = False

        displayer.write(
            historyDisplay,
            self.historyCount,
            1,
            f"{diceSentence} {self.totalDices} ({dices[0]}, {dices[1]})",
        )

    def payTo(self, player, amount):
        self.money = self.money - amount
        player.money = player.money + amount
        displayer.write(
            historyDisplay,
            self.historyCount,
            1,
            f"{namePlayer(self.id)} -> {namePlayer(player.id)} : {amount}",
        )

    def transaction(self, amount):
        displayer.write(
            historyDisplay,
            self.historyCount,
            1,
            f"{win if amount > 0 else lost} {abs(amount)} €",
        )
        self.money = self.money + amount

    def isFamily(self, case):
        idFamily = model.index(case["membership"])
        return bool(
            np.where(
                (
                    np.count_nonzero(self.own[idFamily, : len(model[idFamily]), 0] == 1)
                    == len(model[idFamily])
                )
                & (self.own[idFamily, : len(model[idFamily]), 1] == 0)
            )[0].size
        )

    def isBuilt(self, case):
        return self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 2
        ]

    def moveByDice(self, nbr):
        self.location = self.location + nbr
        if self.location > 40:
            self.transaction(200)
            self.location -= 40

    def moveByCard(self, where, backward=False, moveBackward=False):
        self.loopWhile = True

        if self.location > where and not backward and not moveBackward:
            self.transaction(200)

        self.location = where if not moveBackward else self.location + where

    def moveToJail(self):
        self.forcedToJail = True
        self.inJail = True
        self.turn = False
        self.location = 10

    def outOfJail(self):
        self.inJail = False
        self.countTurnInJail = 0
        self.location = 10

    def moveOutOfJail(self):
        self.outOfJail()
        self.moveByDice(self.totalDices)

    def getPrice(self, case):
        isFamily = self.isFamily(case)
        if case["type"] == "property":
            if isFamily:
                built = self.isBuilt(case["id"])
                if built == 5:
                    return case["hotel"]
                elif built:
                    return case[f"house_{built}"]
                else:
                    return case["rent"] * 2
            return case["rent"]
        elif case["type"] == "station":
            return case["rent"] * np.count_nonzero(
                self.own[model.index(case["membership"]), :, 0]
            )
        else:
            return 4 * self.totalDices if not isFamily else 10 * self.totalDices

    def landOnProperty(self):

        case = cases[self.location]

        if (
            case["type"] == "property"
            or case["type"] == "station"
            or case["type"] == "company"
        ):
            if case["mortgaged"]:
                return ('mortgaged', case["owned"])
            elif case["owned"]:
                return ('owned', case["owned"])
            else:

                x = self.choice([1, 2], [buy, notBuy])

                # Buy
                if x == 1:
                    self.buy(case)

        if case["type"] == "tax":
            self.transaction(-case["price"])

        if case["type"] == "goToJail":
            self.moveToJail()

        if case["type"] == "chance" or case["type"] == "communityChest":

            active = CARDS[case["type"]]
            card = active[0]
            active.append(active.pop(0))
            self.castCard(card, case["name"])

    def endTurn(self):
        self.action = False
        self.__historyCount = 1
        self.countDouble = 0
        self.turn = True
        self.forcedToJail = False
        self.moveOutOfJail = False
        self.tryDouble = False
        self.actions = []
        displayer.refreshElements(actionsDisplay, historyDisplay, textDisplay)

    def castCard(self, card, type):
        card["cast"](self)
        displayer.refreshElement(textDisplay)
        displayer.write(textDisplay, 1, 1, type)
        displayer.write(textDisplay, 2, 1, card["text"])

    def buy(self, case):
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 0
        ] = 1
        cases[case["id"]]["owned"] = self.id
        displayer.write(
            historyDisplay, self.historyCount, 1, f"{buySentence} {case['name']}"
        )
        self.transaction(-case["price"])

    def mortgage(self, case):
        case["mortgaged"] = True
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 1
        ] = 1
        displayer.write(
            historyDisplay, self.historyCount, 1, f"{mortgageSentence} : {case['name']}"
        )
        self.transaction(case["mortgagePrice"])

    def unmortgage(self, case):
        case["mortgaged"] = False
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 1
        ] = 0
        displayer.write(
            historyDisplay,
            self.historyCount,
            1,
            f"{unMortgageSentence} : {case['name']}",
        )
        self.transaction(-case["mortgagePrice"])

    def build(self, case):
        state = (
            "1 hotel"
            if case["built"] == 5
            else f"{case['built']} maison{'s' if case['built'] > 1 else ''}"
        )
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 1
        ] += 1
        case["built"] += 1
        displayer.write(
            historyDisplay, self.historyCount, 1, f"{case['name']} a {state}"
        )
        self.transaction(-case["housePrice"])

    def sell(self, case):
        state = f"{case['built']} maison{'s' if case['built'] > 1 else ''}"
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 1
        ] -= 1
        case["built"] -= 1
        displayer.write(
            historyDisplay, self.historyCount, 1, f"{case['name']} a {state}"
        )
        self.transaction(case["housePrice"] / 2)

    def getIdOfMortgageable(self):
        indexes = np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 0))
        return [model[i][y] for i, y in zip(*indexes)]

    def getIdOfUnmortgageable(self):
        indexes = np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 1))
        return [model[i][y] for i, y in zip(*indexes)]

    def mortgageable(self):
        return np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 0))[0].size > 0

    def unmortgageable(self):
        return np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 1))[0].size > 0

    def getIdOfBuildable(self):
        res = []
        for z in range(len(model)):
            if z != 0 or z != 9:
                indexes = np.where(
                    (
                        np.count_nonzero(self.own[z, : len(model[z]), 0] == 1)
                        == len(model[z])
                    )
                    & (self.own[z, : len(model[z]), 1] == 0)
                    & (
                        np.amin(self.own[z, : len(model[z]), 2])
                        >= self.own[z, : len(model[z]), 2]
                    )
                    & (self.own[z, : len(model[z]), 2] <= 5)
                )[0]
                for i in indexes:
                    res.append(model[z][i])
        return res

    def getIdOfSaleable(self):
        res = []
        for z in range(len(model)):
            if z != 0 or z != 9:
                indexes = np.where(
                    (self.own[z, : len(model[z]), 2] > 0)
                    & (
                        np.amax(self.own[z, : len(model[z]), 2])
                        <= self.own[z, : len(model[z]), 2]
                    )
                )[0]
                for i in indexes:
                    res.append(model[z][i])
        return res

    def checkActions(self):
        self.actions = []

        # Roll dice
        if self.turn and not self.inJail:
            self.actions.append(0)
        # Mortgage
        if self.mortgageable() and not self.forcedToJail:
            self.actions.append(1)
        # Unmortgage
        if self.unmortgageable() and not self.forcedToJail:
            self.actions.append(2)
        # Build
        if bool(self.getIdOfBuildable()) and not self.forcedToJail:
            self.actions.append(3)
        # Sell
        if bool(self.getIdOfSaleable()) and not self.forcedToJail:
            self.actions.append(4)
        # End turn
        if (self.money > 0 and not self.turn and not (self.inJail and not self.tryDouble)) or self.forcedToJail:
            self.actions.append(5)
        # Try Double
        if self.inJail and not self.forcedToJail and not self.tryDouble:
            self.actions.append(6)
        # Pay Fine
        if self.inJail and not self.forcedToJail and not self.tryDouble:
            self.actions.append(7)
        # Use Free Jail Card
        if self.inJail and self.freeJailCard and not self.forcedToJail:
            self.actions.append(8)

        return self.choice(
            self.actions, [f"{ACTIONS[i]}" for i in self.actions]
        )

    def getPriceOfAllBuildingsForTHEFUCKING_Card(self):
        return (
            self.own[self.own[:, :, 2] < 5][:, 2].sum() * 25
            + np.count_nonzero(self.own[:, :, 2] == 5) * 100
        )

    def getPriceOfAllBuildingsForTHEWORSTFUCKING_Card(self):
        return (
            self.own[self.own[:, :, 2] < 5][:, 2].sum() * 40
            + np.count_nonzero(self.own[:, :, 2] == 5) * 115
        )

    # Sorry.... I has to
