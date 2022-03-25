from __future__ import annotations

from curses import initscr, flushinp
from curses.textpad import Textbox
from itertools import cycle
import numpy as np

from Displayer import Displayer
from cards import CARDS
from Tiles import *
from sentences import *
from constants import *

std = initscr()

displayer = Displayer()
(
    actionsDisplay,
    historyDisplay,
    transactionDisplay,
    textDisplay,
    miscellaneousDisplay,
    miscellaneousLeftDisplay,
    miscellaneousRightDisplay,
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
        self.auctioning = False
        self.bankruptcy = False
        self.players: Player[Player] = []
        displayer.player(self)

    def __call__(self, players):
        self.players = players
        displayer.write(historyDisplay, text=f"{currentTurn[LANG](self.name)}")

    def getFreeJailCard(self):
        self.freeJailCard += 1
        displayer.write(historyDisplay, text=f"{getFreeJailCard[LANG]}")

    def useFreeJailCard(self):
        self.freeJailCard -= 1
        displayer.write(historyDisplay, text=f"{useFreeJailCard[LANG]}")

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

    def choice(self, nbr, texts, multiple=False):
        displayer.refreshElement(actionsDisplay)

        for i in range(len(texts)):
            displayer.write(actionsDisplay, y=1 + i, text=f"{nbr[i]} : {texts[i]}")

        while True:
            flushinp()
            try:
                x = std.getkey() if multiple else "0"
                y = std.getkey()
                if y == "q":
                    quit()
                if y == "c":
                    return None
                res = int(x) + int(y)
                if res not in nbr:
                    raise Exception
                return res
            except ValueError and Exception:
                pass
    
    def askBid(self, bidAmount):
        displayer.concat(miscellaneousLeftDisplay, f" {offers[LANG]} : ")
        
        nb = ''
        while True:
            x = std.getch()
            
            if x == 127 and len(nb) > 0:
                nb = nb[:-1]
                coor = miscellaneousLeftDisplay.getyx()
                miscellaneousLeftDisplay.delch(coor[0], coor[1]-1)
                miscellaneousLeftDisplay.refresh()
                
            elif x == 10 and nb != '':
                if int(nb) > bidAmount: break
            elif 48 <= x <= 57:
                nb = f'{nb}{x-48}'
                displayer.concat(miscellaneousLeftDisplay, str(x-48))
            
            
        displayer.concat(miscellaneousLeftDisplay, f' {moneySign[LANG]}')
        return int(nb)
        
        
    def rollDice(self):
        dices = np.random.randint(1, 7, size=2)
        dices = [5, 3]
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
            historyDisplay, text=f"{payToSentence[LANG](player.name)}",
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
        displayer.write(historyDisplay, text=f"{inJail[LANG]}")

    def outOfJail(self):
        self.inJail = False
        self.location = 10
        displayer.write(historyDisplay, text=f"{free[LANG]}")

    def moveOutOfJail(self):
        self.outOfJail()
        self.moveOutOfJailBool = True

    def getPrice(self, case, caseState, double):
        price = 0
        if case["type"] == "property":
            price = (
                case["house_0"] * 2
                if caseState["isFamily"] and not caseState["built"]
                else case[f"house_{caseState['built']}"]
            )
        elif case["type"] == "railroad":
            price = case["rent"] * np.count_nonzero(
                states[SETS.index(case["membership"]), :, 0]
            )
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
                    while (x := self.choice([1, 2], [buy[LANG], auction[LANG]])) is None: pass
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
                historyDisplay, text=drawCards[LANG](displayer.formatName(case["name"]))
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
        displayer.refreshElementWithoutBorder(miscellaneousLeftDisplay)
        while True:
            
            while bidder := next(bidCycled):
                if not bidder.auctioning or bidder.bankruptcy: continue
                else: break
                
            displayer.refreshElementWithoutBorder(miscellaneousRightDisplay)
            displayer.auctionInfo(miscellaneousRightDisplay, bidAmount, bidder.name, case, self.players)   
             
            if nbBidder == 1:
                bidder.winAuction(case, bidAmount)
                break
            
            displayer.write(miscellaneousLeftDisplay, y=0, text=f"{bidder.name}")
            
            while (x := bidder.choice([1, 2], [bid[LANG], out[LANG]])) is None: pass
            
            if x == 1:
                bidAmount = bidder.askBid(bidAmount)
            if x == 2:
                displayer.concat(miscellaneousLeftDisplay, f" {isOut[LANG]}")
                bidder.auctioning = False
                nbBidder -= 1
    
    def winAuction(self, case, bidAmount):
        displayer.write(miscellaneousLeftDisplay, text=f"{self.name} {winAuction[LANG]}")
        self.auctioning = False
        self.buyByAuction(case, bidAmount)
        displayer.refreshCounter('auction')
        
    def endTurn(self):
        self.countDouble = 0
        self.turn = True
        self.forcedToJail = False
        self.tryDouble = False
        displayer.refreshElements(
            actionsDisplay, historyDisplay, textDisplay, miscellaneousDisplay
        )
        displayer.refreshCounter('history')

    def castCard(self, card, type):
        card["cast"](self)
        displayer.refreshElement(textDisplay)
        displayer.write(textDisplay, y=1, text=type)
        displayer.write(textDisplay, y=2, text=f"{card['text'][LANG]}.")

    def buy(self, case):
        states[
            case["idFamily"], np.where(SETS[case["idFamily"]] == case["id"])[0][0], 0
        ] = self.id
        displayer.write(
            historyDisplay,
            text=f"{buySentence[LANG]} {displayer.formatName(case['name'])}",
        )
        self.transaction(-case["price"])
        
    def buyByAuction(self, case, bid):
        states[
            case["idFamily"], np.where(SETS[case["idFamily"]] == case["id"])[0][0], 0
        ] = self.id
        self.transaction(-bid, display=False)

    def mortgage(self, case):
        states[
            case["idFamily"], np.where(SETS[case["idFamily"]] == case["id"])[0][0], 1
        ] = 1
        displayer.write(
            historyDisplay,
            text=f"{displayer.formatName(case['name'])} {mortgageSentence[LANG]}",
        )
        self.transaction(case["mortgagePrice"])

    def unmortgage(self, case):
        states[
            case["idFamily"], np.where(SETS[case["idFamily"]] == case["id"])[0][0], 1
        ] = 0
        displayer.write(
            historyDisplay,
            text=f"{displayer.formatName(case['name'])} {unMortgageSentence[LANG]}",
        )
        self.transaction(-(case["mortgagePrice"] + case["mortgagePrice"] // 10))

    def build(self, case):
        states[
            case["idFamily"], np.where(SETS[case["idFamily"]] == case["id"])[0][0], 2
        ] += 1
        displayer.write(
            historyDisplay,
            text=f"{buyBuildingSentence[LANG]} {displayer.formatName(case['name'])}",
        )
        self.transaction(-case["housePrice"])

    def sell(self, case):
        states[
            case["idFamily"], np.where(SETS[case["idFamily"]] == case["id"])[0][0], 2
        ] -= 1
        displayer.write(
            historyDisplay,
            text=f"{sellBuildingSentence[LANG]} {displayer.formatName(case['name'])}",
        )
        self.transaction(case["housePrice"] // 2)

    def getIdOfMortgageable(self):
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

    def getIdOfUnmortgageable(self):
        indexes = np.where((states[:, :, 0] == self.id) & (states[:, :, 1] == 1))
        return [SETS[i][y] for i, y in zip(*indexes)]

    def getIdOfBuildable(self):
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
                )[0]
                for i in indexes:
                    res.append(SETS[z][i])
        return res

    def getIdOfSaleable(self):
        res = []
        for z in range(len(SETS)):
            if z <= 7:
                indexes = np.where(
                    (states[z, : len(SETS[z]), 2] > 0)
                    & (
                        np.amax(states[z, : len(SETS[z]), 2])
                        <= states[z, : len(SETS[z]), 2]
                    )
                )[0]
                for i in indexes:
                    res.append(SETS[z][i])
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
        # Get out of the game
        if self.bankruptcy:
            actions = [9]

        return self.choice(actions, [f"{ACTIONS[i][LANG]}" for i in actions])

    def turnOver(self, creditor):
        creditor.own += states
        creditor.money += self.money
        creditor.freeJailCard += self.freeJailCard

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
