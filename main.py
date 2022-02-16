import curses
import time
from curses import wrapper

import numpy as np
import random

from classes import *
from functions import *
from sentences import *
from constants import *

from cases import cases
from cards import *


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
    actionsDisplay  = displayElement(12, 30, 1, 0)
    historyDisplay = displayElement(12, 60, 1, 40)
    textDisplay = displayElement(4, 100, 14, 0)

    
    players = [Player(i, namePlayer(i)) for i in range(numberOfPlayers)]
    iterPlayers = players.__iter__()
    # random.shuffle(chanceCards)
    # random.shuffle(communityChestCards)
    
    while players:

        try:
            player = next(iterPlayers)
        except StopIteration:
            iterPlayers = players.__iter__()
            continue

        write(historyDisplay, player.historyCount, 1, f"{tour(player.name)}")
        while True:
            refreshElement(actionsDisplay)
            arrayActions = []
            for i in player.checkActions():
                arrayActions.append(i)
                write(actionsDisplay, len(arrayActions), 1, f"{i}: {ACTIONS[i]}")
            arrayActions.append(6)

            action = ask(int, lambda x: x in arrayActions)

            # Roll Dice
            if action == 0:
                player.dices = random.randint(1, 7, size=2)
                # total = np.sum(player.dices)
                total = 2
                if np.max(player.dices) == np.min(player.dices):
                    player.double = True
                    player.countDouble += 1
                else:
                    player.turn = False
                write(historyDisplay, player.historyCount, 1, f"{diceSentence} {total} ({player.dices[0]}, {player.dices[1]})")
                if player.countDouble == 3:
                    # Go to Jail
                    pass
                
                player.location = player.location + total
                if player.location >= 40: player.location -= 40
                case = cases[player.location]

                if case['type'] == 'property' or case['type'] == 'station' or case['type'] == 'company':
                    if case['mortgaged']:
                        continue
                    elif case['owned'] is not False:
                        owner = players[case['owned']]
                        amount = owner.getPrice(case)
                        player.payTo(owner, amount)
                        write(historyDisplay, player.historyCount, 1, f"{namePlayer(player.id)} -> {namePlayer(owner.id)} : {amount}")
                    else:
                        refreshElement(actionsDisplay)
                        write(actionsDisplay, 1, 1, f"1: {buy}")
                        write(actionsDisplay, 2, 1, f"2: {nobuy}")

                        x = ask(int, lambda x: x in [1, 2])

                        if x == 1:
                            player.own[case['idFamily'], case['membership'].index(case['idProperty']), 0] = 1
                            cases[case['id']]['owned'] = player.id
                            player.transaction(-case['price'])
                            write(historyDisplay, player.historyCount, 1, f"{buySentence} {case['name']}")

                elif case['type'] == 'tax':
                    player.transaction(-case['price'])
                    write(historyDisplay, player.historyCount, 1, f"{lost} {case['price']} €")
                
                elif case['type'] == 'chance' or case['type'] == 'communityChest':
                    current = chanceCards if case['type'] == 'chance' else communityChestCards
                    card = current[0]
                    write(textDisplay, 1, 1, case['name'])
                    write(textDisplay, 2, 1, card['text'])
                    card['cast'](player)
                    write(historyDisplay, player.historyCount, 1, card['historyText'])
                    current.append(current.pop(0))
                
                else:
                    pass
                
            if action == 5:
                player.endTurn()
                refreshElements(actionsDisplay, historyDisplay)
                break
            if action == 6:
                quit()

    return 0


wrapper(main)
