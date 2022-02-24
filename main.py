import curses
from curses import wrapper

import numpy as np
import random

from Players import Player
from sentences import *
from constants import *
from cases import *


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
    numberOfPlayers = 1
    nbrTour = 0

    players = [Player(i, namePlayer(i)) for i in range(numberOfPlayers)]
    iterPlayers = players.__iter__()
    # random.shuffle(CARDS['chance'])
    # random.shuffle(CARDS['communityChest'])

    joueurID = -1

    while players:
        nbrTour += 1

        try:
            player = next(iterPlayers)
            player()

            if player.bankruptcy:
                players.remove(player.id)
                continue
        except StopIteration:
            iterPlayers = players.__iter__()
            continue

        if joueurID == player.id:
            print(congratulations(player.name))
            break

        # joueurID = player.id

        while True:

            if player.bankruptcy:
                break

            if not player.action:
                action = player.checkActions()
            
            # Roll dice
            if action == 0:

                if not player.moveOutOfJail:
                    player.rollDice()
                else:
                    player.moveOutOfJail = True
                    
                player.moveByDice(player.totalDices)

                while True:

                    player.loopWhile = False
                    state, ownerID = player.landOnProperty()

                    if state == 'morgaged':
                        continue
                    
                    elif state == 'owned':
                        owner = players[ownerID]
                        amount = owner.getPrice(case)
                        player.payTo(owner, amount)

                    if not player.loopWhile:
                        break

            # Mortgage
            if action == 1:

                id = player.getIdOfMortgageable()
                x = player.choice(
                    [i for i in range(1, len(id) + 1)], [cases[i]["name"] for i in id]
                )
                if not x:
                    continue
                case = cases[id[x - 1]]
                player.mortgage(case)

            # Unmortage
            if action == 2:

                id = player.getIdOfUnmortgageable()
                x = player.choice(
                    [i for i in range(1, len(id) + 1)], [cases[i]["name"] for i in id]
                )
                if not x:
                    continue
                case = cases[id[x - 1]]
                player.unmortgage(case)

            # Build
            if action == 3:

                id = player.getIdOfBuildable()
                x = player.choice(
                    [i for i in range(1, len(id) + 1)], [cases[i]["name"] for i in id]
                )
                if not x:
                    continue
                case = cases[id[x - 1]]
                player.build(case)

            # Sell
            if action == 4:

                id = player.getIdOfSaleable()
                x = player.choice(
                    [i for i in range(1, len(id) + 1)], [cases[i]["name"] for i in id]
                )
                if not x:
                    continue
                case = cases[id[x - 1]]
                player.sell(case)

            # End of Turn
            if action == 5:
                player.endTurn()
                break

            # Try Double
            if action == 6:
                player.rollDice()

                player.countTurnInJail += 1
                
                if player.double:
                    player.moveOutOfJail()
                    player.turn = False
                    player.action = 0
            
                elif player.countTurnInJail == 3:
                    player.transaction(-50)
                    player.moveOutOfJail()
                    player.action = 0

                player.tryDouble = True

            # Pay Fine
            if action == 7:
                player.outOfJail()
                player.transaction(-50)

            # Use Get out of jail Free
            if action == 8:
                player.outOfJail()
                player.freeJailCard -= 1

            if player.money < 0:
                overdrawn = abs(player.money)
                heritage = 0
                for i in range(len(model)):
                    id = np.where(
                        (player.own[i, : len(model[i]), 0] == 1)
                        & (player.own[i, : len(model[i]), 1] == 0)
                    )[0]
                    for y in id:
                        case = cases[model[i][y]]
                        heritage += (
                            case["mortgagePrice"]
                            + case["housePrice"] / 2 * case["built"] / 2
                        )
                if overdrawn > heritage:
                    player.bankruptcy = True

    return 0


wrapper(main)
