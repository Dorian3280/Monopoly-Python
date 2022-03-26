from __future__ import annotations

from curses import initscr, flushinp
from itertools import cycle
import numpy as np
from Bank import Bank

from Displayer import Displayer
from cards import CARDS
from Tiles import *
from sentences import *
from constants import *

std = initscr()

# Use this to similate pattern of actions you want to get
# e.g. rollDice, buy, endTurn = [0, 1, 5]
# you can also set the next dices numbers
# dices = [3, 2]
debug = []

displayer = Displayer()
(
    actionsDisplay,
    historyDisplay,
    transactionDisplay,
    textDisplay,
    auctionDisplay,
    auctionLeftDisplay,
    auctionRightDisplay,
    tradeDisplay,
    tradeLeftDisplay,
    tradeRightDisplay,
) = displayer()


class Player:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.__money = 1500
        self.__location = 0
        self.double = False
        self.tryDouble = False
        self.payFine = False
        self.inJail = False
        self.forcedToJail = False
        self.forcedToNearest = False
        self.moveOutOfJailBool = False
        self.countTurn = 0
        self.countDouble = 0
        self.totalDices = 0
        self.loopWhile = False
        self.turn = True
        self.freeJailCard = 0
        self.lastDebt = -1
        self.current = False
        self.auctioning = False
        self.bankruptcy = False
        self.players: Player[Player] = []
        self.bank: Bank = None
        displayer.player(self)

    def __call__(self, players, bank):
        self.players = players
        self.current = True
        self.bank = bank
        displayer.write(historyDisplay, text=f"{currentTurn(self.name)[LANG]}")

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

    def getIndexByID(self):
        return next(
            (i for i, player in enumerate(self.players) if player.id == self.id), -1
        )

    def choose(self, nbr, texts, action=False):
        if debug:
            return debug.pop(0)
        displayer.refreshElement(actionsDisplay)

        for i in range(len(texts)):
            displayer.write(actionsDisplay, y=1 + i, text=f"{nbr[i]} : {texts[i]}")

        while True:
            try:
                x = std.getkey()
                if x == "q":
                    quit()
                if x == "c":
                    return None
                if x == "e" and action:
                    return x
                res = int(x)
                if res not in nbr:
                    raise Exception
                return res
            except ValueError and Exception:
                pass

    def chooseNumber(self, text, verify):
        if debug:
            return debug.pop(0)
        flushinp()

        nb = ""
        while True:
            displayer.write(textDisplay, text=f"{text[LANG]} : {nb}")
            x = std.getch()
            if 48 <= x <= 57:
                nb = f"{nb}{x-48}"
            elif x == 127 and len(nb) > 0:
                nb = nb[:-1]
                displayer.refreshElement(textDisplay)
            elif x == 99:
                displayer.refreshElement(textDisplay)
                return "c"
            elif x == 10 and nb != "":
                displayer.refreshElement(textDisplay)
                if verify(int(nb)):
                    break
                nb = ""

        return int(nb)

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
            text=f"{diceSentence[LANG]} {self.totalDices} ({dices[0]}, {dices[1]})",
        )

    def payTo(self, player: Player, amount: int):
        self.lastDebt = player.id
        self.money -= amount
        player.money += amount
        displayer.write(
            historyDisplay, text=f"{payToSentence(player.name)[LANG]}",
        )
        displayer.write(
            transactionDisplay, text=f"{moneySign[LANG]} -{amount}",
        )

    def transaction(self, amount, display=True):
        self.lastDebt = -1
        if display:
            displayer.write(
                transactionDisplay, text=f"{moneySign[LANG]} {amount:+}",
            )
        self.money += amount

    def moveByDice(self, nbr):
        temp = self.location + nbr
        if temp >= TILES.shape[0]:
            displayer.write(
                historyDisplay, text=f"{salary[LANG]}",
            )
            self.transaction(200)
            temp %= TILES.shape[0]
        self.location = temp

    def moveByCard(self, where, backward=False, moveBackward=False):
        self.loopWhile = True

        if self.location > where and not backward and not moveBackward:
            self.transaction(200)

        self.location = where if not moveBackward else self.location + where

    def moveToNearest(self, type):
        last = TILES[TILES["type"] == type].iloc[-1]
        tiles = list(SETS[last["idFamily"]])
        tiles.append(self.location)
        tiles.sort()
        try:
            where = tiles[tiles.index(self.location) + 1]
        except IndexError:
            where = tiles[0]

        if self.location > last["id"]:
            self.transaction(200)

        self.loopWhile = True
        self.forcedToNearest = True
        self.location = where

    def moveToJail(self):
        self.forcedToJail = True
        self.inJail = True
        self.turn = False
        self.location = 10
        displayer.write(historyDisplay, text=f"{moveToJailSentence[LANG]}")

    def outOfJail(self):
        self.inJail = False
        self.location = 10
        displayer.write(historyDisplay, text=f"{outOfFailSentence[LANG]}")

    def moveOutOfJail(self):
        self.moveOutOfJailBool = True
        self.outOfJail()

    def getPrice(self, case, caseState, double):
        price = 0
        if case["type"] == "property":
            price = (
                case["house_0"] * 2
                if caseState["isFamily"] and not caseState["built"]
                else case[f"house_{caseState['built']}"]
            )
        elif case["type"] == "railroad":
            price = case["rent"] * np.count_nonzero(states[case["idFamily"], :, 0])
            if double:
                price *= 2
        else:
            price = (
                4 * self.totalDices
                if not caseState["isFamily"]
                else 10 * self.totalDices
            )
            if double:
                price *= 2

        return price

    def landOnProperty(self):
        case = TILES.loc[self.location]

        if (
            case["type"] == "property"
            or case["type"] == "railroad"
            or case["type"] == "utility"
        ):
            caseState = getState(case)
            if caseState["owned"] >= 0:
                if caseState["owned"] != self.id and not caseState["mortgaged"]:
                    owner: Player = self.players[caseState["owned"]]
                    amount = owner.getPrice(case, caseState, self.forcedToNearest)
                    self.payTo(owner, amount)
            else:
                if not self.forcedToNearest:
                    while (
                        x := self.choose([1, 2], [x[LANG] for x in [buy, auction]])
                    ) is None:
                        pass
                else:
                    x = 1
                    self.forcedToNearest = False
                # Buy
                if x == 1:
                    self.buy(case)
                if x == 2:
                    self.putForAuction(case)

        if case["type"] == "tax":
            self.transaction(-case["price"])

        if case["type"] == "gotojail":
            self.moveToJail()

        if case["type"] == "chance" or case["type"] == "chest":

            displayer.write(
                historyDisplay, text=drawCards(displayer.formatName(case["name"]))[LANG]
            )
            active = CARDS[case["type"]]
            card = active[0]
            active.append(active.pop(0))
            self.castCard(card, displayer.formatName(case["name"]))

        if (
            case["type"] == "start"
            or case["type"] == "visiting"
            or case["type"] == "parking"
        ):
            pass

    def putForAuction(self, case):
        bidAmount = 1
        nbBidder = 0
        for p in self.players:
            if p.bankruptcy == False:
                p.auctioning = True
                nbBidder += 1
        bidCycled = cycle(self.players)
        displayer.refreshElement(auctionDisplay)
        displayer.refreshElementWithoutBorder(auctionLeftDisplay)
        while True:

            while bidder := next(bidCycled):
                if not bidder.auctioning or bidder.bankruptcy:
                    continue
                else:
                    break

            displayer.auctionInfo(bidAmount, bidder.name, case, self.players)

            if nbBidder == 1:
                displayer.refreshElement(auctionDisplay)
                bidder.winAuction(case, bidAmount)
                break

            displayer.write(auctionLeftDisplay, y=0, text=f"{bidder.name}")

            while (x := bidder.choose([1, 2], [bid[LANG], out[LANG]])) is None:
                pass

            if x == 1:
                bidAmount = bidder.chooseNumber(
                    chooseNumberSentence, lambda x: x > bidAmount
                )
                displayer.concat(
                    auctionLeftDisplay,
                    f" {offers[LANG]} : {bidAmount}{moneySign[LANG]}",
                )
            if x == 2:
                displayer.concat(auctionLeftDisplay, f" {isOut[LANG]}")
                bidder.auctioning = False
                nbBidder -= 1

    def winAuction(self, case, bidAmount):
        self.auctioning = False
        self.buyByAuction(case, bidAmount)
        displayer.refreshCounter("auction")

    def endTurn(self):
        self.countDouble = 0
        self.turn = True
        self.forcedToJail = False
        self.tryDouble = False
        self.current = False
        displayer.refreshElements(
            actionsDisplay, historyDisplay, textDisplay, auctionDisplay
        )
        displayer.refreshCounter("history")

    def castCard(self, card, type):
        card["cast"](self)
        displayer.refreshElement(textDisplay)
        displayer.write(textDisplay, y=1, text=type)
        displayer.write(textDisplay, y=2, text=f"{card['text'][LANG]}.")

    def buy(self, case):
        states[case["idFamily"], case["idInFamily"], 0] = self.id
        displayer.write(
            historyDisplay,
            text=f"{buySentence[LANG]} {displayer.formatName(case['name'])}",
        )
        self.transaction(-case["price"])

    def buyByAuction(self, case, bid):
        states[case["idFamily"], case["idInFamily"], 0] = self.id
        displayer.write(
            historyDisplay,
            text=f"{(buySentence if self.current else playerBuySentence(self.name))[LANG]} {displayer.formatName(case['name'])}",
        )
        self.transaction(-bid)

    def actionOnProperty(self, type: str):
        ids = getattr(self, f"getIdOf{type.capitalize()}")()

        id = self.chooseNumber(chooseTileSentence, lambda x: x in ids)
        if id == "c":
            return False

        getattr(self, type)(TILES.loc[id])

    def mortgage(self, case):
        states[case["idFamily"], case["idInFamily"], 1] = 1
        displayer.write(
            historyDisplay,
            text=f"{displayer.formatName(case['name'])} {mortgageSentence[LANG]}",
        )
        self.transaction(case["mortgagePrice"])

    def unmortgage(self, case):
        states[case["idFamily"], case["idInFamily"], 1] = 0
        displayer.write(
            historyDisplay,
            text=f"{displayer.formatName(case['name'])} {unmortgageSentence[LANG]}",
        )
        self.transaction(-(case["mortgagePrice"] + case["mortgagePrice"] // 10))

    def build(self, case):
        states[case["idFamily"], case["idInFamily"], 2] += 1
        if states[case["idFamily"], case["idInFamily"], 2] < 5:
            self.bank.remainingHouses -= 1
        else:
            self.bank.remainingHouses += 4
            self.bank.remainingHotels -= 1
        self.bank()

        displayer.write(
            historyDisplay,
            text=f"{buyBuildingSentence[LANG]} {displayer.formatName(case['name'])}",
        )
        self.transaction(-case["housePrice"])

    def sell(self, case):
        if states[case["idFamily"], case["idInFamily"], 2] == 5:
            self.bank.remainingHotels += 1
            self.bank.remainingHouses -= 4
        else:
            self.bank.remainingHouses += 1
        self.bank()

        states[case["idFamily"], case["idInFamily"], 2] -= 1

        self.bank.remainingHouses += 1
        displayer.write(
            historyDisplay,
            text=f"{sellBuildingSentence[LANG]} {displayer.formatName(case['name'])}",
        )
        self.transaction(case["housePrice"] // 2)

    def getIdOfOwn(self):
        res = []
        for z in range(len(SETS)):
            indexes = np.where(states[z, : len(SETS[z]), 0] == self.id)[0]
            for i in indexes:
                res.append(SETS[z][i])

        return res

    def getIdOfMortgage(self):
        res = []
        for z in range(len(SETS)):
            indexes = np.where(
                (states[z, : len(SETS[z]), 0] == self.id)
                & (states[z, : len(SETS[z]), 1] == 0)
                & np.all(states[z, : len(SETS[z]), 2] == 0)
            )[0]
            for i in indexes:
                res.append(SETS[z][i])

        return res

    def getIdOfUnmortgage(self):
        indexes = np.where((states[:, :, 0] == self.id) & (states[:, :, 1] == 1))
        return [SETS[i][y] for i, y in zip(*indexes)]

    def getIdOfBuild(self):
        res = []
        for z in range(len(SETS)):
            if z <= 7:
                indexes = np.where(
                    np.all(states[z, : len(SETS[z]), 0] == self.id)
                    & np.all(states[z, : len(SETS[z]), 1] == 0)
                    & (
                        np.amin(states[z, : len(SETS[z]), 2])
                        >= states[z, : len(SETS[z]), 2]
                    )
                    & (states[z, : len(SETS[z]), 2] != 5)
                    & (
                        self.bank.remainingHouses > 0
                        if np.any(states[z, : len(SETS[z]), 2] < 4)
                        else self.bank.remainingHotels > 0
                    )
                )[0]
                for i in indexes:
                    res.append(SETS[z][i])
        return res

    def getIdOfSell(self):
        res = []
        for z in range(len(SETS)):
            if z <= 7:
                indexes = np.where(
                    (states[z, : len(SETS[z]), 2] > 0)
                    & (
                        np.amax(states[z, : len(SETS[z]), 2])
                        <= states[z, : len(SETS[z]), 2]
                    )
                    & (
                        self.bank.remainingHouses >= 4
                        if np.any(states[z, : len(SETS[z]), 2] == 5)
                        else True
                    )
                )[0]
                for i in indexes:
                    res.append(SETS[z][i])
        return res

    def giveProperties(self, id, properties):
        print(id, properties, end="")
        for c in properties:
            case = TILES.loc[c]
            states[case["idFamily"], case["idInFamily"], 0] = id

    def getFreeJailCard(self):
        self.freeJailCard += 1
        displayer.write(historyDisplay, text=f"{getFreeJailCard[LANG]}")

    def useFreeJailCard(self):
        self.freeJailCard -= 1
        displayer.write(historyDisplay, text=f"{useFreeJailCard[LANG]}")

    def checkActions(self):
        actions = []

        # Roll dice
        if self.turn and not self.inJail:
            actions.append(0)
        # Mortgage
        if bool(self.getIdOfMortgage()) and not self.forcedToJail:
            actions.append(1)
        # Unmortgage
        if bool(self.getIdOfUnmortgage()) and not self.forcedToJail:
            actions.append(2)
        # Build
        if bool(self.getIdOfBuild()) and not self.forcedToJail:
            actions.append(3)
        # Sell
        if bool(self.getIdOfSell()) and not self.forcedToJail:
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
        # Get out of the game
        if self.bankruptcy:
            actions = [9]

        return self.choose(
            actions, [f"{ACTIONS[i][LANG]}" for i in actions], action=True
        )

    def trade(self):
        ids = [p.id for p in self.players if not p.bankruptcy and not self.id == p.id]

        id = self.chooseNumber(choosePlayerSentence, lambda x: x in ids)
        if id == "c":
            return False

        trader: Player = self.players[id]
        tradeDict = {
            "get": {"money": 0, "properties": []},
            "give": {"money": 0, "properties": []},
        }

        while True:
            displayer.tradeInfo(tradeLeftDisplay, self.name, tradeDict["give"])
            displayer.tradeInfo(tradeRightDisplay, trader.name, tradeDict["get"])

            action = self.choose([1, 2, 3, 4, 5], [f"{a[LANG]}" for a in TRADE])
            concerned = (self, "give") if action in [1, 2] else (trader, "get")

            if action == 1 or action == 3:

                ids = concerned[0].getIdOfOwn()
                id = concerned[0].chooseNumber(chooseTileSentence, lambda x: x in ids)
                if id == "c":
                    continue
                if id in tradeDict[concerned[1]]["properties"]:
                    tradeDict[concerned[1]]["properties"].remove(id)
                else:
                    tradeDict[concerned[1]]["properties"].append(id)

            if action == 2 or action == 4:

                amount = concerned[0].chooseNumber(
                    chooseNumberSentence, lambda x: x <= self.money
                )
                if amount == "c":
                    continue
                tradeDict[concerned[1]]["money"] = amount

            if action == 5:
                response = trader.choose([1, 2], [x[LANG] for x in [accept, decline]])
                if response == 1:
                    self.acceptTrade(trader, tradeDict)
                if response == 2:
                    self.refuseTrade(trader)
                break

            if action is None:
                break

            displayer.refreshElement(tradeDisplay)

        displayer.refreshElement(tradeDisplay)

    def acceptTrade(self, trader: Player, dict):
        trader.money += dict["give"]["money"]
        self.money += dict["get"]["money"]
        trader.money -= dict["get"]["money"]
        self.money -= dict["give"]["money"]

        trader.giveProperties(self.id, dict["get"]["properties"])
        self.giveProperties(trader.id, dict["give"]["properties"])

        displayer.player(self)
        displayer.player(trader)
        displayer.write(historyDisplay, text=f"{trader.name} {acceptTrade[LANG]}")

    def refuseTrade(self, trader):
        displayer.write(historyDisplay, text=f"{trader.name} {declineTrade[LANG]}")

    def getHeritage(self):
        heritage = 0
        for i in range(len(SETS)):
            id = np.where(
                (states[i, : len(SETS[i]), 0] == self.id)  # Own
                & (states[i, : len(SETS[i]), 1] == 0)  # Mortgageable
            )[0]
            for y in id:
                case = TILES[SETS[i][y]]
                heritage += (
                    case["mortgagePrice"] + case["housePrice"] // 2 * case["built"]
                )

        return heritage

    def gameOver(self):
        self.bankruptcy = True
        displayer.write(historyDisplay, text=lostGame[LANG])
        displayer.player(self)

    def birthday(self):
        for player in self.players:
            if self.getIndexByID() != player.id:
                player.payTo(self, 10)

    def elected(self):
        for player in self.players:
            if self.getIndexByID() != player.id:
                self.payTo(player, 50)

    def costFromRepairs(self):
        return (
            states[states[:, :, 2] < 5][:, 2].sum() * 25
            + np.count_nonzero(states[:, :, 2] == 5) * 100
        )

    def costFromRepairsPlus(self):
        return (
            states[states[:, :, 2] < 5][:, 2].sum() * 40
            + np.count_nonzero(states[:, :, 2] == 5) * 115
        )
