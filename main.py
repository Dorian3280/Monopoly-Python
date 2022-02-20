import curses
from curses import wrapper

import numpy as np
import random

from Players import Player
from functions import *
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
    numberOfPlayers = 2

    players = [Player(i, namePlayer(i)) for i in range(numberOfPlayers)]
    iterPlayers = players.__iter__()
    random.shuffle(CARDS['chance'])
    random.shuffle(CARDS['communityChest'])

    joueurID = -1

    while players:

        try:
            player = next(iterPlayers)
            player()

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

        while True:
    
            if player.bankruptcy:
                break

            if player.countTurnInJail == 3:
                player.transaction(-50)
                player.inJail = False
                player.countTurnInJail = 0

            if not player.forced:
                action = player.checkActions()                

            # Roll dice
            if action == 0 or player.forced:
                if not player.forced:

                    total = player.rollDice()

                    # Movement
                    if player.inJail:

                        x = player.choice([1, 2], [wait, getFree])

                        if x == 2:

                            player.transaction(-50)
                            player.inJail = False
                        else:
                            player.countTurnInJail += 1

                        continue

                    if not player.inJail:
                        player.moveByDice(total)

                case = cases[player.location]
                
                if case['type'] == 'property' or case['type'] == 'station' or case['type'] == 'company':
                    if case['mortgaged']:
                        continue
                    elif case['owned'] is not False:
                        owner = players[case['owned']]
                        amount = owner.getPrice(case)
                        player.payTo(owner, amount)
                    else:

                        x = player.choice([1, 2], [buy, notBuy])

                        # Buy
                        if x == 1:
                            player.buy(case)

                if case['type'] == 'tax':
                    player.transaction(-case['price'])
                
                if case['type'] == 'goToJail':
                    player.moveToJail()

                if case['type'] == 'chance' or case['type'] == 'communityChest' or player.forced:
                    if player.forced:
                        player.forced = False
                        if not case['type'] == 'chance' and not case['type'] == 'communityChest':
                            continue
                    active = CARDS[case['type']]
                    card = active[0]
                    active.append(active.pop(0))

                    player.castCard(card, case['name'])
            
            # Mortgage
            if action == 1:

                id = player.getIdOfMortgageable()
                x = player.choice([i for i in range(1, len(id)+1)], [cases[i]['name'] for i in id])
                case = cases[id[x-1]]
                player.mortgage(case)

            # Unmortage
            if action == 2:

                id = player.getIdOfUnmortgageable()
                x = player.choice([i for i in range(1, len(id)+1)], [], [cases[i]['name'] for i in id])
                case = cases[id[x-1]]
                player.unmortgage(case)

            # Build
            if action == 3:

                id = player.getIdOfBuildable()
                x = player.choice([i for i in range(1, len(id)+1)], [cases[i]['name'] for i in id])
                case = cases[id[x-1]]
                player.build(case)

            # Sell
            if action == 4:

                id = player.getIdOfSaleable()
                x = player.choice([i for i in range(1, len(id)+1)], [cases[i]['name'] for i in id])
                case = cases[id[x-1]]
                player.sell(case)

            # End of Turn
            if action == 5:
                player.endTurn()
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
