import curses
import numpy as np

from cases import *
from sentences import *
from constants import *
from Displayer import Displayer

std = curses.initscr()

displayer = Displayer()
(
    actionsDisplay,
    historyDisplay,
    transactionDisplay,
    infoDisplay,
    textDisplay,
) = displayer()


class Player:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.__money = 1500
        self.__location = 0
        self.own = np.zeros((10, 4, 3), dtype=int)
        self.double = False
        self.tryDouble = False
        self.payFine = False
        self.inJail = False
        self.forcedToJail = False
        self.moveOutOfJailBool = False
        self.countTurn = 0
        self.countDouble = 0
        self.totalDices = 0
        self.loopWhile = False
        self.turn = True
        self.freeJailCard = 0
        self.lastDebt = False
        self.bankruptcy = False
        self.players = []
        displayer.player(self)

    def __call__(self, players, nbrTour):
        self.players = players
        displayer.write(historyDisplay, text=f"{currentTurn(self.name)}")
        displayer.write(infoDisplay, text=f"{turn} n°{nbrTour}")

    def __str__(self) -> str:
        return f"id : {self.id}\nturn : {self.turn}\nforcedToJail : {self.forcedToJail}\ninJail : {self.inJail}\ndouble : {self.double}\nmoveOutOfJailBool : {self.moveOutOfJailBool}\ncountTurn : {self.countTurn}\ntryDouble : {self.tryDouble}\npayFine : {self.payFine}"

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
    def location(self):
        return self.__location

    @location.setter
    def location(self, x):
        self.__location = x
        displayer.player(self)

    def choice(self, nbr, texts, multiple=False):
        displayer.refreshElement(actionsDisplay)

        for i in range(len(texts)):
            displayer.write(actionsDisplay, y=1 + i, text=f"{nbr[i]} : {texts[i]}")

        while True:
            curses.flushinp()
            try:
                x = std.getkey() if multiple else "0"
                y = std.getkey()
                if y == "q":
                    quit()
                if y == "c":
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
            text=f"{diceSentence} {self.totalDices} ({dices[0]}, {dices[1]})",
        )

    def payTo(self, player, amount):
        self.lastDebt = player.id
        self.money = self.money - amount
        player.money = player.money + amount
        displayer.write(
            historyDisplay,
            text=f"{landOnSentence(namePlayer(player.id))}",
        )
        displayer.write(
            transactionDisplay,
            text=f"-{amount} €",
        )

    def transaction(self, amount):
        self.lastDebt = False
        displayer.write(
            transactionDisplay, text=f"{amount} €",
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
        temp = self.location + nbr
        if temp > 39:
            displayer.write(
                historyDisplay,
                text=f"{salary}",
            )
            self.transaction(200)
            temp -= 40
        self.location = temp

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
        displayer.write(historyDisplay, text=f"{inJail}")

    def outOfJail(self):
        self.inJail = False
        self.location = 10
        displayer.write(historyDisplay, text=f"{free}")

    def moveOutOfJail(self):
        self.outOfJail()
        self.moveOutOfJailBool = True

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
            if case["owned"]:
                owner = self.players[case["owned"]]
                amount = owner.getPrice(case)
                self.payTo(owner, amount)
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

            displayer.write(historyDisplay, text=drawCards(case["name"]))
            active = CARDS[case["type"]]
            card = active[0]
            active.append(active.pop(0))
            self.castCard(card, case["name"])

    def endTurn(self):
        self.countDouble = 0
        self.turn = True
        self.forcedToJail = False
        self.tryDouble = False
        displayer.refreshElements(
            actionsDisplay, historyDisplay, transactionDisplay, textDisplay
        )
        displayer.refreshHistoryCount()

    def castCard(self, card, type):
        card["cast"](self)
        displayer.refreshElement(textDisplay)
        displayer.write(textDisplay, y=1, text=type)
        displayer.write(textDisplay, y=2, text=card["text"])

    def buy(self, case):
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 0
        ] = 1
        cases[case["id"]]["owned"] = self.id
        displayer.write(historyDisplay, text=f"{buySentence} {case['name']}")
        self.transaction(-case["price"])

    def mortgage(self, case):
        case["mortgaged"] = True
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 1
        ] = 1
        displayer.write(historyDisplay, text=f"{mortgageSentence} : {case['name']}")
        self.transaction(case["mortgagePrice"])

    def unmortgage(self, case):
        case["mortgaged"] = False
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 1
        ] = 0
        displayer.write(
            historyDisplay, text=f"{unMortgageSentence} : {case['name']}",
        )
        self.transaction(-(case["mortgagePrice"]+case["mortgagePrice"]//10))

    def build(self, case):
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 2
        ] += 1
        case["built"] += 1
        displayer.write(
            historyDisplay,
            text=f"{buyHouseSentence if case['built'] < 5 else buyHotelSentence} {case['name']})",
        )
        self.transaction(-case["housePrice"])

    def sell(self, case):
        self.own[
            model.index(case["membership"]), case["membership"].index(case["id"]), 2
        ] -= 1
        case["built"] -= 1
        displayer.write(
            historyDisplay,
            text=f"{sellHouseSentence if case['built'] < 4 else sellHotelSentence} {case['name']}",
        )
        self.transaction(case["housePrice"] // 2)

    def getIdOfMortgageable(self):
        res = []
        for z in range(len(model)):
            indexes = np.where(
                (self.own[z, : len(model[z]), 0] == 1)
                & (self.own[z, : len(model[z]), 1] == 0)
                & np.all(self.own[z, : len(model[z]), 2] == 0)
            )[0]
            for i in indexes:
                res.append(model[z][i])

        return res

    def getIdOfUnmortgageable(self):
        indexes = np.where((self.own[:, :, 0] == 1) & (self.own[:, :, 1] == 1))
        return [model[i][y] for i, y in zip(*indexes)]

    def getIdOfBuildable(self):
        res = []
        for z in range(len(model)):
            if 0 < z < 9:
                indexes = np.where(
                    np.all(self.own[z, : len(model[z]), 0] == 1)
                    & np.all(self.own[z, : len(model[z]), 1] == 0)
                    & (
                        np.amin(self.own[z, : len(model[z]), 2])
                        >= self.own[z, : len(model[z]), 2]
                    )
                    & (self.own[z, : len(model[z]), 2] != 5)
                )[0]
                for i in indexes:
                    res.append(model[z][i])
        return res

    def getIdOfSaleable(self):
        res = []
        for z in range(len(model)):
            if 0 < z < 9:
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
        actions = []

        # Roll dice
        if self.turn and not self.inJail:
            actions.append(0)
        # Mortgage
        if bool(self.getIdOfMortgageable()) and not self.forcedToJail:
            actions.append(1)
        # Unmortgage
        if bool(self.getIdOfUnmortgageable()) and not self.forcedToJail:
            actions.append(2)
        # Build
        if bool(self.getIdOfBuildable()) and not self.forcedToJail:
            actions.append(3)
        # Sell
        if bool(self.getIdOfSaleable()) and not self.forcedToJail:
            actions.append(4)
        # End turn
        if (
            (
                self.money > 0
                and not self.turn
                and not (self.inJail and not self.tryDouble)
            )
            or self.forcedToJail
            or (0 < self.countTurn < 3 and self.payFine)
        ):
            actions.append(5)
        # Try Double
        if self.inJail and not self.forcedToJail and not self.tryDouble:
            actions.append(6)
        # Pay Fine
        if self.inJail and not self.forcedToJail and not self.tryDouble:
            actions.append(7)
        # Use Free Jail Card
        if self.inJail and self.freeJailCard and not self.forcedToJail:
            actions.append(8)

        return self.choice(actions, [f"{ACTIONS[i]}" for i in actions])

    def gameOver():
        displayer.write(historyDisplay, text=lost)

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
