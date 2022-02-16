import curses
import time
from curses import wrapper

import numpy as np

from classes import *
from functions import *
from sentences import *
from constants import *

from cases import cases
from chanceCards import chanceCards
from communityChestCards import communityChestCards


def main(std) -> int:
    RESOLUTION = curses.LINES, curses.COLS
    # std.addstr(RESOLUTION[0] // 2, RESOLUTION[1] // 2 - len(welcome) // 2, welcome)
    # std.addstr(
    #     RESOLUTION[0] // 2 + 1,
    #     RESOLUTION[1] // 2 - len(askNumberOfPlayers) // 2,
    #     askNumberOfPlayers,
    # )
    # std.refresh()
    # numberOfPlayers = ask(int, lambda x: 2 <= x <= 4)
    numberOfPlayers = 2
    std.clear()
    std.refresh()

    write(std, 0, 4, titleActions)
    write(std, 0, 65, titleHistory)
    actionsDisplay  = displayElement(15, 30, 1, 0)
    historyDisplay = displayElement(15, 60, 1, 40)
    
    players = [Player(i, namePlayer(i)) for i in range(numberOfPlayers)]
    
    while players:

        player = next(players.__iter__())

        write(historyDisplay, 1, 1, f"{tour(player.name)}")
        while True:
            arrayActions = []
            for i in player.checkActions():
                arrayActions.append(i)
                write(actionsDisplay, len(arrayActions), 1, f"{i}: {ACTIONS[i]}")

            action = ask(int, lambda x: x in arrayActions)
            # action = 0

            # Roll Dice
            if action == 0:
                player.dices = random.randint(1, 7, size=2)
                total = np.sum(player.dices)
                # total = 6
                if np.max(player.dices) == np.min(player.dices):
                    player.double = True
                    player.countDouble += 1
                else:
                    player.turn = False
                write(historyDisplay, 2, 1, f"{diceSentence} {total} ({player.dices[0]}, {player.dices[1]})")
                if player.countDouble == 3:
                    # Go to Jail
                    pass
                
                player.location = player.location + total
                case = cases[player.location]
                if case['type'] == 'property':
                    if case['mortgaged']:
                        refreshElement(actionsDisplay)
                        continue
                    elif case['owned'] is not False:
                        owner = players[case['owned']]
                        amount = case[owner.checkState(case)]
                        player.payTo(owner, amount)
                        write(historyDisplay, 3, 1, f"{namePlayer(player.id)} -> {namePlayer(owner.id)} : {amount}")
                    refreshElement(actionsDisplay)
                    write(actionsDisplay, 1, 1, f"1: {buy}")
                    write(actionsDisplay, 2, 1, f"2: {nobuy}")
                    x = ask(int, lambda x: x in [1, 2])
                    # x = 1
                    if x == 2:
                        refreshElement(actionsDisplay)
                        continue
                    if x == 1:
                        player.own[case['idFamily'], case['membership'].index(case['idProperty']), 0] = 1
                        cases[case['id']]['owned'] = player.id
                        player.transaction(-case['price'])
                        write(historyDisplay, 3, 1, f"{buySentence} {case['name']}")
                        refreshElement(actionsDisplay)
                        continue
            if action == 5:
                refreshElements(actionsDisplay, historyDisplay)
                end()
                break
    
            end()

        end()

    return 0


wrapper(main)
