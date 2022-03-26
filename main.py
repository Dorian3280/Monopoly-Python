from curses import wrapper
from itertools import cycle
from Players import Player
from Displayer import Displayer
from Tiles import *
from sentences import *
from constants import *


def main(std) -> int:

    Displayer.initColor()

    numberOfPlayers = NB_PLAYERS
    players = [Player(i, f"{genName[LANG]} {i+1}") for i in range(numberOfPlayers)]

    cycled = cycle(players)
    lastPlayer = -1
    while True:
        player = next(cycled)
        player(players)

        if player.bankruptcy:
            continue

        if lastPlayer == player.id:
            print(congratulations(players[0].name)[LANG])
            break

        lastPlayer = player.id

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
                if not player.actionOnProperty("mortgage"):
                    continue

            # Unmortage
            if action == 2:
                if not player.actionOnProperty("unmortgage"):
                    continue

            # Build
            if action == 3:
                if not player.actionOnProperty("build"):
                    continue

            # Sell
            if action == 4:
                if not player.actionOnProperty("sell"):
                    continue

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
                break

            if action == "e":
                player.trade()

            if player.money < 0:
                overdrawn = abs(player.money)
                heritage = player.getHeritage()
                if overdrawn > heritage:
                    if player.lastDebt != -1:
                        id = player.lastDebt.getIndexByID()
                        player.turnOver(players[id])

                    player.gameOver()

    return 0


wrapper(main)
