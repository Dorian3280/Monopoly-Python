import curses
import time
from curses import wrapper

import numpy as np
import random

from classes import *
from functions import *
from sentences import *
from constants import *
from cases import *
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

    actionsDisplay, historyDisplay, textDisplay, choiceDisplay = display()

    players = [Player(i, namePlayer(i)) for i in range(numberOfPlayers)]
    iterPlayers = players.__iter__()
    # random.shuffle(chanceCards)
    # random.shuffle(communityChestCards)

    joueurID = -1

    while players:

        try:
            player = next(iterPlayers)
            if player.bankruptcy:
                players.remove(player.id)
                break
        except StopIteration:
            iterPlayers = players.__iter__()
            continue

        if joueurID == player.id:
            print(f'Congratulations to {player.name} ! You won the game !!!')
            break
        joueurID = player.id

        write(historyDisplay, player.historyCount, 1, f"{tour(player.name)}")

        while True:
            refreshElement(actionsDisplay)
            if player.bankruptcy:
                break

            if player.countTurn == 3:
                player.transaction(-50)
                player.inJail = False
                player.countTurn = 0

            if player.extraMove is False:    
                arrayActions = []
                for i in player.checkActions():
                    arrayActions.append(i)
                    write(actionsDisplay, len(arrayActions), 1, f"{i}: {ACTIONS[i]}")
                action = ask(int, lambda x: x in arrayActions)

            # Roll dice
            if action == 0 or player.extraMove is not False:
                if player.extraMove is False:
                    player.dices = random.randint(1, 7, size=2)
                    # total = np.sum(player.dices)
                    total = 6
                    if np.max(player.dices) == np.min(player.dices):
                        player.countDouble += 1
                        if player.countDouble == 3:
                            player.countDouble = 0
                            player.goToJail()
                            continue
                        player.double = True
                    else:
                        player.turn = False
                    write(historyDisplay, player.historyCount, 1, f"{diceSentence} {total} ({player.dices[0]}, {player.dices[1]})")
                    if player.countDouble == 3:
                        # Go to Jail
                        pass

                # Movement
                if player.inJail and not player.double:

                    refreshElement(actionsDisplay)
                    loopWrite(actionsDisplay, 1, 1, [wait, getFree])
                    x = ask(int, lambda x: x in [1, 2])

                    if x == 2:
                        player.transaction(-50)
                        player.inJail = False
                    else:
                        player.countTurn += 1

                    continue

                player.move(total, player.extraMove)

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
                        loopWrite(actionsDisplay, 1, 1, [buy, nobuy])
                        x = ask(int, lambda x: x in [1, 2])

                        if x == 1:
                            player.own[model.index(case['membership']), case['membership'].index(case['id']), 0] = 1
                            cases[case['id']]['owned'] = player.id
                            player.transaction(-case['price'])
                            write(historyDisplay, player.historyCount, 1, f"{buySentence} {case['name']}")

                elif case['type'] == 'tax':
                    player.transaction(-case['price'])
                    write(historyDisplay, player.historyCount, 1, f"{lost} {case['price']} €")
                
                elif case['type'] == 'chance' or case['type'] == 'communityChest':
                    refreshElement(textDisplay)
                    active = chanceCards if case['type'] == 'chance' else communityChestCards
                    card = active[0]
                    card['cast'](player)
                    active.append(active.pop(0))
                    write(historyDisplay, player.historyCount, 1, card['historyText'])
                    loopWrite(textDisplay, 1, 1, [case['name'], card['text']])
                
                elif case['type'] == 'goToJail':
                    player.goToJail()
                    pass
            
            # Mortgage 
            if action == 1:

                id = player.getIdOfMortgageable()
                loopWrite(choiceDisplay, 1, 1, [cases[i]['name'] for i in id])
                x = ask(int, lambda x: x in range(1, len(id)+1))
                case = cases[id[x-1]]
                player.mortgage(case)
                write(historyDisplay, player.historyCount, 1, f"{mortgageSentence} : {case['name']}")
                write(historyDisplay, player.historyCount, 1, f"{win} {case['mortgagePrice']} €")

            # Unmortage
            if action == 2:

                id = player.getIdOfUnmortgageable()
                loopWrite(choiceDisplay, 1, 1, [cases[i]['name'] for i in id])
                x = ask(int, lambda x: x in range(1, len(id)+1))
                case = cases[id[x-1]]
                player.unmortgage(case)
                write(historyDisplay, player.historyCount, 1, f"{unMortgageSentence} : {case['name']}")
                write(historyDisplay, player.historyCount, 1, f"{lost} {case['mortgagePrice']} €")

            # Build
            if action == 3:
                id = player.getIdOfBuildable()
                loopWrite(choiceDisplay, 1, 1, [cases[i]['name'] for i in id])
                x = ask(int, lambda x: x in range(1, len(id)+1))
                case = cases[id[x-1]]
                player.build(case)
                case['built'] += 1
                state = "1 hotel" if case['built'] == 5 else f"{case['built']} maison{'s' if case['built'] > 1 else ''}"
                write(historyDisplay, player.historyCount, 1, f"{case['name']} a {state}")
                write(historyDisplay, player.historyCount, 1, f"{lost} {case['housePrice']} €")

            # Sell
            if action == 4:
                id = player.getIdOfBuildable()
                loopWrite(choiceDisplay, 1, 1, [cases[i]['name'] for i in id])
                x = ask(int, lambda x: x in range(1, len(id)+1))
                case = cases[id[x-1]]
                player.sell(case)
                case['built'] -= 1
                state = f"{case['built']} maison{'s' if case['built'] > 1 else ''}"
                write(historyDisplay, player.historyCount, 1, f"{case['name']} a {state}")
                write(historyDisplay, player.historyCount, 1, f"{win} {case['housePrice']/2} €")

            # End of Turn
            if action == 5:
                player.endTurn()
                refreshElements(actionsDisplay, historyDisplay, textDisplay, choiceDisplay)
                break

            # Quit
            if action == 6:
                quit()

            # Use Get out of jail Free 
            if action == 7:
                player.free -= 1
                player.inJail = False
            
            if player.money < 0:
                overdrawn = abs(player.money)
                heritage = 0
                for i in range(len(model)):
                    id = np.where((player.own[i, :len(model[i]), 0] == 1) & (player.own[i, :len(model[i]), 1] == 0))[0]
                    for y in id:
                        case = cases[model[i][y]]
                        heritage += case['mortgagePrice'] + case['housePrice']/2*case['built']
                if overdrawn > heritage:
                    player.bankruptcy = True

    return 0


wrapper(main)
