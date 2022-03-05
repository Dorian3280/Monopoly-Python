import curses
from curses import wrapper

import numpy as np
import random

from Players import Player
from Displayer import Displayer
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
    
    Displayer.initColor()
    numberOfPlayers = 2
    nbrTour = 0

    players = [Player(i, namePlayer(i)) for i in range(numberOfPlayers)]
    iterPlayers = players.__iter__()
    random.shuffle(CARDS["chance"])
    random.shuffle(CARDS["communityChest"])

    while players:
        nbrTour += 1

        try:
            if len(players) == 1: raise Exception
            player = next(iterPlayers)
            player(players, nbrTour)

        except StopIteration:
            iterPlayers = players.__iter__()
            continue
        except Exception:
            print(congratulations(players[0].name))
            break

        if player.inJail or player.countTurn:
            player.countTurn += 1

        while True:

            if player.bankruptcy:
                player.gameOver()
                players.remove(player.id)
                std.getch()
                break

            action = 0

            if player.moveOutOfJailBool is False:
                action = player.checkActions()

            # Roll dice
            if action == 0:

                if player.payFine:
                    player.payFine = False
                    player.countTurn = 0

                if not player.moveOutOfJailBool:
                    player.rollDice()
                else:
                    player.moveOutOfJailBool = False

                player.moveByDice(player.totalDices)

                while True:

                    player.loopWhile = False
                    player.landOnProperty()

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

                if player.double:
                    player.moveOutOfJail()
                    player.turn = False

                elif player.countTurn == 3:
                    player.moveOutOfJail()
                    player.transaction(-50)

                player.tryDouble = True

            # Pay Fine
            if action == 7:
                player.payFine = True
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
                        (
                            player.own[i, : len(model[i]), 0] == 1
                        )  # Mortgageable property
                        & (player.own[i, : len(model[i]), 1] == 0)  # Buildings
                    )[0]
                    for y in id:
                        case = cases[model[i][y]]
                        heritage += (
                            case["mortgagePrice"]
                            + case["housePrice"] // 2 * case["built"]
                        )
                if overdrawn > heritage:
                    if player.lastDebt is not False:
                        players[player.lastDebt].own = (
                            players[player.lastDebt].own + player.own
                        )
                        players[player.lastDebt].money = (
                            players[player.lastDebt].money + player.money
                        )
                        players[player.lastDebt].freeJailCard = (
                            players[player.lastDebt].freeJailCard + player.freeJailCard
                        )

                    player.bankruptcy = True

    return 0


wrapper(main)
