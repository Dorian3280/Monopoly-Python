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

        self.actions = self.displayElement(11, 36, 1, 1)  # actionsDisplay
        self.history = self.displayElement(11, 69, 1, 38)  # historyDisplay
        self.text = self.displayElement(4, 106, 12, 1)  # textDisplay
        self.auction = self.displayElement(15, 93, 1, 108)  # auctionDisplay
        self.auctionLeft = self.auction.derwin(13, 44, 1, 1)
        self.auctionRight = self.auction.derwin(13, 44, 1, 44)
        self.trade = self.displayElement(15, 93, 1, 108)  # tradeDisplay
        self.tradeLeft = self.auction.derwin(13, 44, 1, 1)
        self.tradeRight = self.auction.derwin(13, 44, 1, 44)
        self.transaction = self.history.derwin(11, 10, 0, 59)  # transactionDisplay

        self.write(std, 0, 7, text=TITLES["action"][LANG])
        self.write(std, 0, 65, text=TITLES["history"][LANG])
        self.write(
            std, 0, 138, text=f"{TITLES['auction'][LANG]} / {TITLES['trade'][LANG]}"
        )

        self.countLineHistory = 0
        self.countLineAuction = 0

    def __call__(self):
        self.refreshElement(self.actions)
        self.refreshElement(self.history)
        self.refreshElement(self.text)
        self.refreshElement(self.auction)
        return (
            self.actions,
            self.history,
            self.transaction,
            self.text,
            self.auction,
            self.auctionLeft,
            self.auctionRight,
            self.trade,
            self.tradeLeft,
            self.tradeRight,
        )

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

    @staticmethod
    def align(str: str, w, surroundBy=" ", nb=1, align="^"):
        str = f"{' '*nb}{str}{' '*nb}"
        return f"{str:{surroundBy}{align}{w-2}s}"

    def addArrow(self, str, right):
        arrow = "← " if right else " →"
        return f"{arrow if right else ''}{str}{arrow if not right else ''}"

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
        w = 50
        x = 1 + player.id * w

        pos = (
            self.formatName(TILES.loc[player.location]["name"])
            if not player.location == 10
            else self.formatName(
                TILES.loc[player.location]["name"], visiting=(not player.inJail)
            )
        )
        win = self.displayElement(38, w, 16, x)
        if player.bankruptcy:
            self.write(
                win, 9, 1, text=self.align(player.name, win.getmaxyx()[1], "x"), color=5
            )
            self.write(win, 11, 1, text=f"{bankruptcy[LANG]:^47s}", color=5)
        else:
            self.write(win, 1, 1, text=self.align(player.name, win.getmaxyx()[1], "*"))
            self.write(win, 3, 2, text=f"ID : {player.id}")
            self.write(win, 4, 2, text=f"{money[LANG]} : {player.money} €")
            self.write(
                win,
                5,
                2,
                text=f"{location[LANG]} : {pos}",
                color=TILES.loc[player.location]["idColor"],
            )
            self.write(win, 7, 1, text=self.align(owning[LANG], win.getmaxyx()[1], "+"))

            indexes = np.where(states[:, :, 0] == player.id)

            for i, (familyID, caseID) in enumerate(zip(*indexes)):
                case = TILES.loc[SETS[familyID][caseID]]
                self.write(
                    win,
                    9 + i,
                    2,
                    text=f"{case['id']} - {self.formatName(case['name'])}{self.propertiesOfPlayer(case)}",
                    color=case["idColor"],
                )

    def write(self, component, y=1, x=2, text="", color=10):
        if component == self.history:
            if self.countLineHistory > 9:
                self.countLineHistory = 1
                self.refreshElement(component)
                if component == self.history:
                    self.refreshElement(self.transaction)

            else:
                self.countLineHistory += 1

            y = self.countLineHistory

        if component == self.transaction:
            y = self.countLineHistory

        if component == self.auctionLeft:
            if self.countLineAuction > 9:
                self.countLineAuction = 1
                self.refreshElement(component)

            else:
                self.countLineAuction += 1

            y = self.countLineAuction

        component.addstr(y, x, text, curses.color_pair(color))
        component.refresh()

    def concat(self, component, text, color=10):
        component.addstr(text, curses.color_pair(color))
        component.refresh()

    def refreshCounter(self, type):
        if type == "history":
            self.countLineHistory = 0
        if type == "auction":
            self.countLineAuction = 0

    def refreshElement(self, element):
        element.clear()
        element.border()
        element.refresh()

    def refreshElementWithoutBorder(self, element):
        element.clear()
        element.refresh()

    def refreshElements(self, *elements):
        for element in elements:
            element.clear()
            element.border()
            element.refresh()

    def createAuctionElement(self):
        elem = curses.newwin(12, 35, 2, 165)
        elem.border()
        return elem

    def auctionInfo(self, bidAmount, name, case, players):
        self.refreshElementWithoutBorder(self.auctionRight)
        self.write(
            self.auctionRight,
            y=0,
            text=self.align("Info", self.auctionRight.getmaxyx()[1], "-"),
        )
        self.write(self.auctionRight, 2, 2, text=f"{objectOfAuction[LANG]} :")
        self.write(
            self.auctionRight,
            3,
            7,
            text=self.formatName(case["name"]),
            color=case["idColor"],
        )
        self.write(
            self.auctionRight,
            4,
            2,
            text=f"{bidAmountSentence[LANG]} : {bidAmount} {moneySign[LANG]}",
        )
        self.write(self.auctionRight, 5, 2, text=currentTurn(name)[LANG])
        self.write(self.auctionRight, 7, 15, text=f"{remains[LANG]}")
        remaining = [p.name for p in players if p.auctioning and not p.bankruptcy]
        for i, p in enumerate(remaining):
            self.write(self.auctionRight, 8 + i, 2, text=f"{p}")

    def tradeInfo(self, component, name, data):
        align = "<" if component == self.tradeRight else ">"
        self.write(component, y=0, text=self.align(name, component.getmaxyx()[1], "-"))
        if data["money"] > 0:
            self.write(
                component,
                y=2,
                text=self.align(
                    self.addArrow(f"{data['money']}", component == self.tradeRight),
                    component.getmaxyx()[1],
                    align=align,
                ),
            )
        for i, p in enumerate(data["properties"]):
            case = TILES.loc[p]
            self.write(
                component,
                y=3 + i,
                text=self.align(
                    self.addArrow(
                        self.formatName(case["name"]), component == self.tradeRight
                    ),
                    component.getmaxyx()[1],
                    align=align,
                ),
                color=case["idColor"],
            )
