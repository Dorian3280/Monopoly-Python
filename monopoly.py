from itertools import cycle

from Bank import Bank
from Players import Player


class Monopoly:
    """Monopoly Game"""

    def __init__(self):
        self.bank = Bank()
        self.players = [
            Player(i, f"|*.uwu.*| {i+1}", self.bank)
            for i in range(2)
        ]

        self.cycled = cycle(self.players)
        self.last_player = -1

    def start_game(self):

        while True:
            player = next(self.cycled)
            player(self.players)

            if player.bankruptcy:
                continue

            if self.last_player == player.id:
                print(player.win())
                break

            self.last_player = player.id

            if player.in_jail or player.count_turn:
                player.count_turn += 1

            while True:

                action = 0
                
                if not player.is_moving_out_of_jail:
                    action = player.check_actions()
                print('action : ', action)
                # Roll dice
                if action == 0:

                    if player.pay_fine:
                        player.pay_fine = False
                        player.count_turn = 0

                    if not player.is_moving_out_of_jail:
                        player.roll_dice()
                    else:
                        player.is_moving_out_of_jail = False

                    player.move_by_dice(player.total_dices)

                    while True:

                        player.loop_while = False
                        player.land_on_property()

                        if not player.loop_while:
                            break

                # Mortgage
                if action == 1:
                    if not player.action_on_property("mortgage"):
                        continue

                # Unmortage
                if action == 2:
                    if not player.action_on_property("unmortgage"):
                        continue

                # Build
                if action == 3:
                    if not player.action_on_property("build"):
                        continue

                # Sell
                if action == 4:
                    if not player.action_on_property("sell"):
                        continue

                # End of Turn
                if action == 5:
                    player.end_turn()
                    break

                # Try Double
                if action == 6:
                    player.roll_dice()

                    if player.double:
                        player.move_out_of_jail()
                        player.turn = False

                    elif player.count_turn == 3:
                        player.move_out_of_jail()
                        player.transaction(-50)

                    player.try_double = True

                # Pay Fine
                if action == 7:
                    player.pay_fine = True
                    player.out_of_jail()
                    player.transaction(-50)

                # Use Get out of jail Free
                if action == 8:
                    player.out_of_jail()
                    player.use_free_jail_card()

                # Get out of the game
                if action == 9:
                    player.end_turn()
                    break

                if action == "e":
                    player.trade()

                if player.money < 0:
                    overdrawn = abs(player.money)
                    heritage = player.get_heritage()
                    if overdrawn > heritage:
                        player.give_properties(
                            player.last_debt, player.get_own_property()
                        )
                        if player.last_debt != -1:
                            winner = self.players[player.last_debt]
                            winner.money += player.money
                            winner.free_jail_card_counter += (
                                player.free_jail_card_counter
                            )

                        player.game_over()
