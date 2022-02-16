import curses
import time
from curses import wrapper

from numpy import number

from functions import *
from sentences import *
from cases import cases
from chanceCards import chanceCards
from communityChestCards import communityChestCards


def main(stdscr) -> int:
    # RESOLUTION = curses.LINES, curses.COLS
    # stdscr.addstr(RESOLUTION[0] // 2, RESOLUTION[1] // 2 - len(welcome) // 2, welcome)
    # stdscr.addstr(
    #     RESOLUTION[0] // 2 + 1,
    #     RESOLUTION[1] // 2 - len(askNumberOfPlayers) // 2,
    #     askNumberOfPlayers,
    # )
    # stdscr.refresh()
    # numberOfPlayers = ask(int, lambda x: 2 <= x <= 4)
    numberOfPlayers = 2
    stdscr.clear()
    stdscr.refresh()

    players = initializePlayers(numberOfPlayers)

    while players:
        player = next(players.__iter__())
        while True:
            stdscr.addstr(f"{tour(player.name)}\n")
            arrayActions = []
            for i in player.checkActions():
                arrayActions.append(i)
                stdscr.addstr(f"{i}: {ACTIONS[i]}")

            action = ask(int, lambda x: x in arrayActions)

            print(action)
            quit()

    return 0


wrapper(main)
