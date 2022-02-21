import curses
from constants import TITLES, COLORS
from cases import *

std = curses.initscr()


class Displayer:
    def __init__(self):

        self.actions = self.displayElement(12, 40, 1, 0)  # actionsDisplay
        self.history = self.displayElement(12, 60, 1, 43)  # historyDisplay
        self.text = self.displayElement(4, 190, 15, 0)  # textDisplay
        self.write(std, 0, 4, TITLES["action"])
        self.write(std, 0, 57, TITLES["history"])
        self.write(std, 0, 157, TITLES["player"])
        self.write(std, 14, 85, TITLES["text"])

    def __call__(self):
        self.refreshElement(self.actions)
        self.refreshElement(self.history)
        self.refreshElement(self.text)
        return self.actions, self.history, self.text

    def displayElement(self, h, w, y, x):
        element = curses.newwin(h, w, y, x)
        element.border()
        return element

    def player(self, player):
        win = self.displayElement(4, 40, 1 + player.id * 4, 150)
        self.write(win, 1, 1, f"Joueur {player.id} : {player.money} €")
        self.write(
            win,
            2,
            1,
            f"{cases[player.location]['name'] if not player.inJail else cases[player.location]['namebis']}",
            COLORS[cases[player.location]["idColor"]],
        )

    def write(self, component, y, x, text, color=COLORS[9]):
        component.addstr(y, x, text, color)
        component.refresh()

    def loopWrite(self, component, y, x, indices, texts, color=COLORS[9]):
        for i in range(len(texts)):
            self.write(component, y + i, x, f"{indices[i]} : {texts[i]}", color)

    def refreshElement(self, element):
        element.clear()
        element.border()
        element.refresh()

    def refreshElements(self, *elements):
        for element in elements:
            element.clear()
            element.border()
            element.refresh()
