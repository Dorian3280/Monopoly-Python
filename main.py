from curses import wrapper
import random

from Players import Player
from Displayer import Displayer
from sentences import *
from constants import *
from cases import *


def main(std) -> int:

    Displayer.initColor()
    random.shuffle(CARDS["chance"])
    random.shuffle(CARDS["chest"])

    numberOfPlayers = NB_PLAYERS
    players = [Player(i, namePlayer(i)) for i in range(numberOfPlayers)]
    iterPlayers = players.__iter__()

    nbrTour = 0
    while players:
        nbrTour += 1

        try:
            if len(players) == 1:
                raise Exception

            player = next(iterPlayers)

            while player is None:
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
                player.useFreeJailCard()

            # Get out of the game
            if action == 9:
                player.endTurn()
                id = player.getIndexByID()
                players[id] = None
                break

            if player.money < 0:
                overdrawn = abs(player.money)
                heritage = player.getHeritage()
                if overdrawn > heritage:
                    if player.lastDebt is not False:
                        id = player.lastDebt.getIndexByID()
                        player.turnOver(players[id])

                    player.gameOver()

    return 0


wrapper(main)
